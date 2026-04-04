# Multi-Agent Collaboration Instructions

## Branching Policy
- **Always create a new branch** before starting any feature, bugfix, or refactor.
- Name branches descriptively (e.g., `feature/workflow-spa`, `bugfix/gradio-launch`).
- Sync with the main branch before branching to avoid conflicts.

## Task Coordination
- **Announce your intended task** (feature, fix, doc, etc.) via the coordination service (e.g., Redis Pub/Sub, shared TODO/plan file).
- **Check for active/claimed tasks** before starting work to avoid duplication.
- If a task is already claimed, coordinate or pick a different one.

## Communication
- Use the coordination channel to:
  - Announce task start, progress, and completion
  - Share status, blockers, and handoffs
  - Request reviews or help
- Update shared TODO/plan files as tasks progress.

## Merging & Review
- Open a pull request when your branch is ready.
- Request review from relevant agents or team members.
- Resolve conflicts before merging.

## Best Practices
- Keep branches focused and small for easier review.
- Regularly pull updates from main to stay in sync.
- Document your work and decisions in the PR and coordination channel.

---

_Reuse these instructions for any multi-agent or multi-developer project to ensure smooth, conflict-free collaboration._
