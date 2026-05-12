# vaultwares-pipelines

> For company-wide rules, read `vaultwares-docs/AGENTS.md` first.

<!-- VAULT-THEMES-SUBMODULE:START -->
## vault-themes Submodule

Before UI, branding, or token work, read:

- `vault-themes/AGENTS.md`
- `vault-themes/CONTEXT.md`
<!-- VAULT-THEMES-SUBMODULE:END -->
 
## VaultWares Repo Instructions

### Editing rule

You may modify files locally in this repository whenever the task calls for it.
What is restricted on `main` is creating Git commits or pushing changes unless the user explicitly asks for that in the current turn.

### Standalone repo rule

When a task involves `vault-themes`, `vaultwares-agentciation`, or `vaultwares_agentciation`, make the real change in the standalone repository itself.
If you encounter a nested copy or submodule mirror here, use it as context only and do not treat it as the authoritative source for the change.

### Practical intent

The goal of the rule is to prevent accidental edits in the wrong checkout, not to discourage local file changes.
Edit the right file in the right repo, verify it, and stop before committing on `main` unless explicitly requested.
