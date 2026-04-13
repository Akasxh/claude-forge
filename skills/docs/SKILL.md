---
name: docs
description: Dispatch the Documentation & Knowledge Team on any documentation task. Auto-detects project language, framework, and existing docs. Use this skill IMMEDIATELY when the user asks to generate docs, update README, write API docs, create changelogs, document architecture, check doc accuracy, or improve code comments.
---

# Documentation Team dispatch

1. Read `~/.claude/agent-memory/docs-lead/MEMORY.md`.
2. Read `~/.claude/agents/docs/docs-lead.md` — adopt as behavioral contract.
3. Create session workspace at `<cwd>/.claude/teams/docs/<slug>/`.
4. Execute: Detection → Plan → Author (reader→writer→tester→reviewer) → Evaluator → Retrospector.
5. Deliver verified, tested documentation.
