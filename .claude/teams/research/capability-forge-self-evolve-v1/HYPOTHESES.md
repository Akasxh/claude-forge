# HYPOTHESES.md — Capability Forge architecture

Four competing architectures. Attack with evidence.

## H1. Single specialist `forge-lead`

One all-capable meta-agent file. Reads roster, picks gap, researches, writes SKILL.md, tests, registers, logs to MEMORY.md. Uses the Skill tool to invoke `skill-creator` for the canonical eval loop.

**Pro**: Minimum complexity. Maps cleanly to adopted-persona runtime constraint. One MEMORY.md. No PROTOCOL.md. Fast to build.

**Con**: Concentrates many lenses (inventory, research-request, authoring, testing, curation) in one file. Prompt bloat risk. Testing + adversarial corpus vetting are hard to co-locate with authoring.

## H2. Mini-team `teams/forge/` with lead + 4-5 specialists

`forge-lead` orchestrates `forge-inventory`, `forge-scout` (internet aggregator), `forge-author` (SKILL.md writer), `forge-tester` (runs skill-creator eval loop), `forge-curator` (registers + INDEX.md + MEMORY.md). Shared workspace at `~/.claude/teams/forge/<slug>/`.

**Pro**: Clean separation mirrors Research Team v2 pattern. Each specialist owns one failure mode. Testable. Scales (can add `forge-mcp-scout` later).

**Con**: More files. Still needs adopted-persona. Overlap risk with research-lead's cartographer/github-miner (must be scoped).

## H3. Skill-loop inside research-retrospector

Extend retrospector: after session close, if lessons imply missing capability, retrospector authors draft SKILL.md to `~/.claude/skills/_forge-drafts/`. Akash reviews and promotes.

**Pro**: Zero new persona files. Reuses existing MEMORY.md pipeline. Lesson → skill loop is elegant.

**Con**: Retrospector scoped for cross-session learning, not skill authoring. Conflates roles. Skill authoring is multi-step (draft → test → iterate) — doesn't fit single-pass retrospector. No mechanism for internet aggregation Akash explicitly asked for.

## H4. Orthogonal meta-layer, no workspace, reads-only

A reference file (`~/.claude/forge/PLAYBOOK.md`) any agent or the main session reads on demand. Not an agent. Invoked by a manual `/forge` slash command launching a fresh Claude session with the playbook loaded and a pointer to the roster.

**Pro**: Zero runtime complexity. No subagent-spawning limits. Every session can invoke.

**Con**: No persistent memory, no self-improvement loop, no clear owner. Akash's ask was for something that *develops its own skills* — that implies state, roster, learning loop. H4 has none.

## Scoring dimensions

1. Runtime fit (respects no-sub-sub-spawn)
2. Separation of concerns (inventory/research/author/test/curate)
3. Self-improvement capacity (MEMORY.md, lesson loop)
4. First-session ergonomics (writable in one session, smoke-testable)
5. Downstream-of-research discipline (does not duplicate research-lead's work)

## Seed verdict (TENTATIVE, pre-evidence)

H2 looks strongest on paper: mirrors Research Team v2 pattern, cleanly separates Akash's named phases, obvious MEMORY.md home per specialist. H1 is strong backup if specialist count proves overkill for first-session smoke test.

Specialists: attack this. Primary sources = the official skill-creator plugin structure (one skill, three sub-agent reference files, not a team), the Voyager skill-library paper, the claude-code-skills marketplace's `engineering-team/` directory layout, and the MemGPT/ACE self-improvement pattern the retrospector already implements. If H1 wins on primary evidence, surface it. If H2 wins because Research Team v2 proved the pattern at the relevant scale, surface that. Falsification, not ratification.
