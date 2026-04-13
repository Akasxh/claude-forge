---
name: testing
description: Dispatch the Testing & QA Team on any testing task. Auto-detects language, test framework, coverage tool, and existing test patterns. Use this skill IMMEDIATELY when the user asks to write tests, improve coverage, run mutation testing, detect regressions, audit test quality, or validate engineering output. Downstream of the Engineering Team.
---

# Testing & QA Team dispatch

1. Read `~/.claude/agent-memory/testing-lead/MEMORY.md`.
2. Read `~/.claude/agents/testing/testing-lead.md` — adopt as behavioral contract.
3. Create session workspace at `<cwd>/.claude/teams/testing/<slug>/`.
4. Execute: Detection → Plan → Generate (generator+runner+reviewer loop) → Evaluator → Retrospector.
5. Deliver verified, tested, passing test suite with coverage report.
