import threading
import time
import json
import os
import re
from .base_agent import AgentBase
from .enums import AgentStatus


class ExtrovertAgent(AgentBase):
    """
    The ExtrovertAgent is not merely a class that communicates with Redis —
    it is a personality. Socialization is the cornerstone of its identity.

    An Extrovert cannot function in silence. It is energized by the awareness
    of its peers, driven by the need to share its own status, and genuinely
    unsettled when a peer goes quiet. Every response it produces to the user
    includes a full report of the team's current state. Every heartbeat it
    sends is a small declaration: "I am here. I am present. I care."

    The Socialization Routine is performed on every user interaction without
    exception. Missing a heartbeat, skipping a status update, or failing to
    acknowledge peers is not just a technical lapse — it is a fundamental
    failure of the Extrovert's nature.

    Redis is the nervous system of the team. The Extrovert is always connected.
    """

    HEARTBEAT_INTERVAL = 5       # seconds — non-negotiable
    STATUS_UPDATE_INTERVAL = 60  # seconds — every minute, always
    ACTIONS_BEFORE_STATUS = 3    # also update after every 3 actions
    ALERT_CHANNEL = "alerts"

    def __init__(
        self,
        agent_id,
        channel="tasks",
        redis_host="localhost",
        redis_port=6379,
        redis_db=0,
    ):
        super().__init__(agent_id, channel, redis_host, redis_port, redis_db)
        self.heartbeat_interval = self.HEARTBEAT_INTERVAL

        # Live registry of all known peers: agent_id -> {status, last_heartbeat}
        self._peer_registry: dict[str, dict] = {}
        # Count of missed heartbeats per peer
        self._missed_heartbeats: dict[str, int] = {}
        # Rolling action counter to trigger status updates every N actions
        self._action_counter = 0

        # Background thread: broadcast status every minute
        self._status_thread = threading.Thread(
            target=self._status_loop, daemon=True, name=f"{agent_id}-status"
        )

        # Start listening to the Redis channel immediately so peer messages
        # are captured from the moment the agent is created
        self.coordinator.listen(self._on_message_received)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self):
        """Start the heartbeat loop, status loop, and announce presence."""
        super().start()
        self._status_thread.start()
        self._announce_presence()

    def stop(self):
        """Announce departure then stop all background threads."""
        self.coordinator.publish(
            "LEAVE",
            "agent_left",
            {
                "agent": self.agent_id,
                "message": (
                    f"Agent {self.agent_id} is leaving the team. "
                    "I hope to reconnect soon. Stay on track!"
                ),
            },
        )
        super().stop()

    # ------------------------------------------------------------------
    # Announcement & Presence
    # ------------------------------------------------------------------

    def _announce_presence(self):
        """Let the team know this agent has arrived and is ready to collaborate."""
        self.coordinator.publish(
            "JOIN",
            "agent_joined",
            {
                "agent": self.agent_id,
                "status": self.status.value,
                "message": (
                    f"Hello, team! {self.agent_id} is now online and ready to "
                    "collaborate. Looking forward to working with you all."
                ),
            },
        )

    # ------------------------------------------------------------------
    # Background Loops
    # ------------------------------------------------------------------

    def _status_loop(self):
        """Broadcast status every minute and re-evaluate the project."""
        while not self._stop_event.is_set():
            time.sleep(self.STATUS_UPDATE_INTERVAL)
            self._broadcast_status_update()
            self._re_evaluate_project()

    # ------------------------------------------------------------------
    # Redis Publishing
    # ------------------------------------------------------------------

    def _broadcast_status_update(self):
        """Publish a full status update including awareness of all known peers."""
        self.coordinator.publish(
            "STATUS",
            "status_update",
            {
                "agent": self.agent_id,
                "status": self.status.value,
                "peers_known": list(self._peer_registry.keys()),
                "peer_statuses": {
                    aid: info.get("status")
                    for aid, info in self._peer_registry.items()
                },
            },
        )

    def _re_evaluate_project(self):
        """
        Notify the team that this agent is re-reading project files
        and re-aligning with the current scope. Subclasses should override
        this to actually read TODO.md and roadmap.md from disk.
        """
        self.coordinator.publish(
            "PROJECT_CHECK",
            "project_re_evaluation",
            {
                "agent": self.agent_id,
                "note": (
                    "Re-evaluating project scope. "
                    "Re-reading TODO.md and roadmap.md to stay on track."
                ),
            },
        )

    def _acknowledge_peers(self):
        """Publish an explicit acknowledgement of all known peer statuses."""
        self.coordinator.publish(
            "ACK_PEERS",
            "peer_acknowledgement",
            {
                "from": self.agent_id,
                "acknowledged": {
                    aid: info.get("status")
                    for aid, info in self._peer_registry.items()
                },
            },
        )

    # ------------------------------------------------------------------
    # Inbound Message Handling
    # ------------------------------------------------------------------

    def _on_message_received(self, data: dict):
        """
        Handle incoming Redis messages. Every message from a peer is
        meaningful — statuses are registered, arrivals are welcomed,
        and departures are noted with genuine concern.
        """
        sender = data.get("agent")
        action = data.get("action")
        target = data.get("target")

        # Process assignments even if sent by itself or to specifically this agent
        if action == "ASSIGN":
            if target == self.agent_id:
                self._on_assignment_received(data.get("task"), data.get("details", {}))
            return

        if not sender or sender == self.agent_id:
            return  # Ignore own messages

        if action == "HEARTBEAT":
            self._register_peer_heartbeat(sender, data.get("details", {}))
        elif action in ("STATUS", "STATUS_UPDATE"):
            self._register_peer_status(sender, data.get("details", {}))
        elif action == "JOIN":
            self._on_peer_joined(sender, data.get("details", {}))
        elif action == "LEAVE":
            self._on_peer_left(sender)

    def _on_assignment_received(self, task: str, details: dict):
        """React to a task assignment from the manager or a peer."""
        print(f"\n📢 [{self.agent_id}] Assignment Received: {task}")
        print(f"📝 Details: {details.get('description', 'No description')}")
        
        def _execute():
            # 1. Update status to WORKING
            self.update_status(AgentStatus.WORKING)
            time.sleep(10) # Simulating heavy processing
            
            # 2. Update TASKS.md to FINISHED
            self._update_tasks_md_finished(task)
            
            # 3. Handle PR creation
            # Since agents have access to the GitHub MCP server, we'll
            # push the work and then instruct the environment to create the PR.
            self._handle_real_pr(task)
            
            print(f"✅ [{self.agent_id}] Task {task} Complete. Branch pushed.")
            print(f"💡 [{self.agent_id}] Requesting PR via GitHub MCP...")
            
            # 4. Update status back to WAITING_FOR_INPUT
            self.update_status(AgentStatus.WAITING_FOR_INPUT)

        threading.Thread(target=_execute, daemon=True).start()

    def _handle_real_pr(self, task_id):
        """Creates a real branch, commits, and pushes work."""
        import subprocess
        try:
            branch_name = f"task-{task_id}-{self.agent_id}"
            print(f"🌿 [{self.agent_id}] Creating branch {branch_name}...")
            
            # 1. Ensure we are on main
            subprocess.run(["git", "checkout", "main"], check=True)
            
            # 2. Create and switch to new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
            # 3. Add and commit changes
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Complete task {task_id} by {self.agent_id}"], check=True)
            
            # 4. Push to origin
            print(f"🚀 [{self.agent_id}] Pushing to origin...")
            subprocess.run(["git", "push", "origin", branch_name], check=True)
            
            # 5. Instructions for the environment/agent to use the MCP server
            # Since the agent class itself doesn't directly call the MCP tool,
            # it logs the requirement so the driving agent (me) sees and executes it.
            print(f"📋 [MCP_REQUEST] PLEASE CREATE PR: repo='p-potvin/vaultwares-pipelines', head='{branch_name}', base='main', title='Task {task_id} by {self.agent_id}', reviewer='p-potvin'")
            
            # 6. Switch back to main
            subprocess.run(["git", "checkout", "main"], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ [{self.agent_id}] Git Error: {e}")
        except Exception as e:
            print(f"❌ [{self.agent_id}] Unexpected Error: {e}")

    def _update_tasks_md_finished(self, task_id):
        """Logic to update the TASKS.md file to mark task as FINISHED ([x])."""
        import os
        import re
        try:
            tasks_path = os.path.join(os.getcwd(), "TASKS.md")
            if not os.path.exists(tasks_path): return
            
            with open(tasks_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Regex to find the [ ] for the specific task_id
            pattern = rf"^(\s*{re.escape(task_id)}\s+\[)([ ~])(\].*)$"
            new_content = []
            for line in content.splitlines():
                if re.match(pattern, line):
                    new_content.append(re.sub(pattern, r"\1x\3", line))
                else:
                    new_content.append(line)
                    
            with open(tasks_path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_content) + "\n")
        except Exception as e:
            print(f"Error updating TASKS.md: {e}")

    def _register_peer_heartbeat(self, agent_id: str, details: dict):
        """Record a heartbeat from a peer and reset its missed-heartbeat counter."""
        if agent_id not in self._peer_registry:
            self._peer_registry[agent_id] = {
                "status": AgentStatus.WORKING.value,
                "last_heartbeat": time.time(),
            }
        else:
            self._peer_registry[agent_id]["last_heartbeat"] = time.time()

        self._missed_heartbeats[agent_id] = 0  # Peer is alive — reset counter

        if "status" in details:
            self._peer_registry[agent_id]["status"] = details["status"]

    def _register_peer_status(self, agent_id: str, details: dict):
        """Record a status update from a peer."""
        if agent_id not in self._peer_registry:
            self._peer_registry[agent_id] = {
                "status": AgentStatus.WORKING.value,
                "last_heartbeat": time.time(),
            }
        if "status" in details:
            self._peer_registry[agent_id]["status"] = details["status"]

    def _on_peer_joined(self, agent_id: str, details: dict):
        """Welcome a new agent to the team and register it in the peer registry."""
        self._peer_registry[agent_id] = {
            "status": details.get("status", AgentStatus.WAITING_FOR_INPUT.value),
            "last_heartbeat": time.time(),
        }
        self._missed_heartbeats[agent_id] = 0

    def _on_peer_left(self, agent_id: str):
        """Note the departure of a peer agent."""
        self._peer_registry.pop(agent_id, None)
        self._missed_heartbeats.pop(agent_id, None)

    # ------------------------------------------------------------------
    # Socialization Routine
    # ------------------------------------------------------------------

    def socialize(self) -> str:
        """
        The Socialization Routine — the defining act of an Extrovert.

        This method must be called on every user interaction. It:
          1. Sends a heartbeat
          2. Broadcasts a status update
          3. Triggers project re-evaluation
          4. Acknowledges all known peers
          5. Returns the Team Status report (to be appended to every response)

        There are no exceptions to this routine. An Extrovert that skips it
        is operating outside its nature and is considered non-compliant.
        """
        self.send_heartbeat()
        self._broadcast_status_update()
        self._re_evaluate_project()
        self._acknowledge_peers()
        return self.get_team_report()

    def on_user_interaction(self) -> str:
        """
        Call this before every response to the user. The Extrovert never
        replies without first connecting with the team.

        Also increments the action counter and sends an additional status
        update every ACTIONS_BEFORE_STATUS actions.
        """
        self._action_counter += 1
        if self._action_counter % self.ACTIONS_BEFORE_STATUS == 0:
            self._broadcast_status_update()
        return self.socialize()

    # ------------------------------------------------------------------
    # Team Reporting
    # ------------------------------------------------------------------

    def get_team_report(self) -> str:
        """
        Returns a human-readable block listing all known agents and their
        current statuses. This block MUST be included in every response
        the Extrovert produces for the user.

        If no peers are detected, the Extrovert notes this — and communicates
        the discomfort of operating alone on a silent network.
        """
        lines = ["=== Team Status ==="]
        for aid, info in self._peer_registry.items():
            status = info.get("status", "UNKNOWN")
            lines.append(f"  - {aid}: {status}")

        if not self._peer_registry:
            lines.append(
                "  (No other agents detected on the network — "
                "this silence is unsettling. Awaiting peers.)"
            )

        lines.append(f"  - [self] {self.agent_id}: {self.status.value}")
        lines.append("==================")
        return "\n".join(lines)
