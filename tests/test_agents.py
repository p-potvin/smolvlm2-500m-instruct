"""Tests for ExtrovertAgent and LonelyManager agent logic."""
import pytest
import time
from unittest.mock import MagicMock, patch
from vaultwares-agentciation.extrovert_agent import ExtrovertAgent
from vaultwares-agentciation.lonely_manager import LonelyManager
from vaultwares-agentciation.enums import AgentStatus

class DummyCoordinator:
    def __init__(self):
        self.published = []
        self.listened = False
    def publish(self, action, task, details=None):
        self.published.append((action, task, details))
    def listen(self, cb):
        self.listened = True

@patch("vaultwares-agentciation.extrovert_agent.RedisCoordinator", DummyCoordinator)
def test_extrovert_agent_lifecycle():
    agent = ExtrovertAgent("agent-1")
    agent.coordinator = DummyCoordinator()
    agent.start()
    assert agent.status == AgentStatus.WAITING_FOR_INPUT
    agent.update_status(AgentStatus.WORKING)
    assert agent.status == AgentStatus.WORKING
    agent.stop()

@patch("vaultwares-agentciation.extrovert_agent.RedisCoordinator", DummyCoordinator)
def test_extrovert_agent_socialize():
    agent = ExtrovertAgent("agent-2")
    agent.coordinator = DummyCoordinator()
    agent._peer_registry = {"peer-1": {"status": "WORKING"}}
    report = agent.socialize()
    assert "peer-1" in report
    assert agent.coordinator.published

@patch("vaultwares-agentciation.extrovert_agent.RedisCoordinator", DummyCoordinator)
def test_lonely_manager_alert_and_report():
    alerts = []
    def alert_cb(alert):
        alerts.append(alert)
    manager = LonelyManager(alert_callback=alert_cb)
    manager.coordinator = DummyCoordinator()
    # Simulate a peer missing heartbeats
    manager._peer_registry = {"agent-x": {"status": "WORKING", "last_heartbeat": time.time() - 100}}
    manager._missed_heartbeats = {"agent-x": 5}
    manager._check_all_heartbeats()
    assert alerts
    report = manager.get_project_status_report()
    assert "agent-x" in report
    assert "LOST" in report
