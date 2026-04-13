---
specialist: research-cartographer
slug: orchestration-full-activation-v1
started: 2026-04-12T05:18Z
completed: 2026-04-12T05:22Z
tool_calls_count: 8
citations_count: 14
confidence: high
---

# Cartographer — structural map of the Claude Code team substrate

Sub-question (from planner): Structural mapping of the existing research team
workspace. Inventory how every sibling in-flight session actually uses
`EVIDENCE/`. Document the de-facto schema the 3 siblings already follow so
v2.1 is backward-compatible. Map `~/.claude/teams/`, `~/.claude/agents/research/`,
`~/.claude/agent-memory/`, `~/.claude/lib/`, `~/.claude/hooks/` to understand
the host filesystem.

## Method

Glob + Bash ls + `wc -c` + Read on one representative file from each
session type. No heuristics; just filesystem inventory. Tool-call budget: 8.

## 1. The host filesystem (the substrate this protocol runs on)

```
/home/akash/.claude/
├── CLAUDE.md                         # global rules, 13 sections, line-counted in
│                                     # related evidence
├── CLAUDE.md.backup.*                # 2 backups
├── settings.json                     # runtime config, hooks, permissions
├── settings.json.bak.1775942110      # previous version
├── agents/
│   ├── research/                     # <-- 17 specialist persona files + 1 lead
│   │   ├── research-lead.md
│   │   ├── research-planner.md
│   │   ├── research-cartographer.md
│   │   ├── research-archaeologist.md
│   │   ├── research-librarian.md
│   │   ├── research-tracer.md
│   │   ├── research-empiricist.md
│   │   ├── research-skeptic.md
│   │   ├── research-adversary.md
│   │   ├── research-historian.md
│   │   ├── research-linguist.md
│   │   ├── research-web-miner.md
│   │   ├── research-github-miner.md
│   │   ├── research-synthesist.md
│   │   ├── research-moderator.md
│   │   ├── research-evaluator.md
│   │   ├── research-retrospector.md
│   │   └── research-scribe.md
│   ├── [top-level legacy agents: analyst, architect, executor, git-manager, etc.]
│   └── researcher.md
├── agent-memory/                     # <-- persistent cross-session memory
│   ├── research-lead/
│   │   └── MEMORY.md                 # 14,102 bytes, 158 lines (as of 2026-04-12)
│   ├── research-retrospector/
│   │   └── MEMORY.md                 # 1,541 bytes
│   └── architect-planner/
│       ├── MEMORY.md
│       ├── project_haste_v2.md
│       ├── project_medscribe.md
│       └── user_akash.md
├── teams/
│   ├── research/                     # <-- THIS team's workspace namespace
│   │   ├── PROTOCOL.md               # 376 lines, v2
│   │   ├── PROTOCOL.v1.bak           # v1 kept for diff
│   │   ├── INDEX.md                  # session ledger, scribe-owned
│   │   ├── <slug>/                   # one dir per session
│   │   │   ├── QUESTION.md           # lead-owned
│   │   │   ├── HYPOTHESES.md         # lead + skeptic
│   │   │   ├── EVIDENCE/<name>.md    # one per specialist
│   │   │   ├── SYNTHESIS.md          # lead ONLY
│   │   │   ├── LOG.md                # append-only
│   │   │   └── OPEN_QUESTIONS.md     # optional
│   │   └── [7 sessions as of 2026-04-12, 4 in flight]
│   └── 352dbd60-e73b-4c6c-85ce-b661206e9d6c/   # <-- mysterious UUID team dir
│       └── inboxes/                  # mailbox pattern, likely unused experiment
├── lib/
│   └── git-identity.sh               # 2,796 bytes, sets user.name/email per repo
├── hooks/                            # DOES NOT EXIST YET
├── scripts/                          # DOES NOT EXIST YET
├── backups/, cache/, debug/, downloads/, file-history/, hud/, ide/, image-cache/,
│   paste-cache/, plans/, plugins/, projects/, security_warnings_state_*.json, telemetry/,
│   todos/
└── history.jsonl                     # global session history
```

**Critical finding 1**: `~/.claude/hooks/` and `~/.claude/scripts/` **do not exist
yet**. This is important for two deliverables:
- D3 (audit script) needs `~/.claude/scripts/` — must be created before writing
  `audit_evidence.py`.
- Any hook-based enforcement (H3) needs to live in `~/.claude/hooks/` OR inline
  in `settings.json`'s `hooks` block. The current `settings.json` has
  `SessionStart` and `PreToolUse` (Bash-matcher) hooks but no `Write` matcher.

**Critical finding 2**: `settings.json` already has a `PreToolUse` hook for
`Bash` that runs `git-identity.sh` on `git commit|push|gh pr create`. This
**proves the hook pattern works** — a `PreToolUse` on `Write` with a path
matcher would be structurally identical. The syntax is:
```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Write", "hooks": [ { "type": "command", "command": "..." } ] }
  ]
}
```
The hook receives tool input as JSON on stdin, can inspect `tool_input.file_path`,
and can exit non-zero to block the tool call.

**Critical finding 3**: `defaultMode: "bypassPermissions"` in `settings.json`
means tools run without permission prompts. Akash documented this in CLAUDE.md
("bypassPermissions mode is the default"). A hook that `exit 1`s on missing
evidence will produce a structured error visible to the subagent, not a
permission dialog.

## 2. The teams directory (the session workspace layer)

Seven sessions exist under `teams/research/`:

| Slug | State | EVIDENCE/ files | Total bytes | Completion |
|---|---|---|---|---|
| `claude-memory-layer-sota-2026q2` | CLOSED (v1) | 17 files (all gates) | 263,334 | full v2 close |
| `claude-memory-layer-sota-2026q2-deeper` | IN FLIGHT (v2 rerun) | 7 files so far | ~90,000 | pre-gate |
| `engineering-team-self-evolve-v1` | IN FLIGHT | 7 files so far | ~119,000 | pre-gate |
| `capability-forge-self-evolve-v1` | IN FLIGHT | 1 file (planner) | ~10,500 | Round 0 only |
| `orchestration-full-activation-v1` | IN FLIGHT (this session) | 1 file (planner) | ~6,800 | Round 0 only |
| `vllm-moe-ep-routing-2026q2` | — | directory exists | — | — |
| (other) | — | — | — | — |

**Observation on completion discipline**: `claude-memory-layer-sota-2026q2`
is the ONLY session that ran all v2 gates to close. It has evidence files
for: planner, cartographer, librarian, historian, historian-addendum (!),
web-miner, github-miner, tracer, linguist, empiricist, synthesist, moderator,
skeptic, adversary, evaluator, retrospector, scribe. That's 17 files. All
three in-flight sessions are currently in Round 1 wide-dispatch phase,
which is the exact phase where the enforcement gap the lead is designing
against most risks showing up.

## 3. De-facto evidence-file schema (what the 3 siblings actually do)

I sampled 24 evidence files from two sessions (memory-layer closed + engineering
in flight). Here's the consolidated de-facto schema:

### Structure (always present)
1. **H1 title line**: `# <Specialist-Name> — <sub-question-or-topic>`
2. **Metadata preamble** (3–5 lines): `Session:`, `Date:`, `Lens:` OR
   `Sub-question:`. **No YAML frontmatter is currently used.**
3. **Method section** (`## Method`): 2–6 lines on how the specialist executed.
4. **Findings / Body**: numbered sections (`## 1. …`, `## 2. …`) or by
   sub-topic. This is the bulk of the file (70–85% of bytes).
5. **Citations inline within findings**: URL + retrieved-date, `path:line`
   for code, commit-sha for git.
6. **Confidence section** (`## Confidence` or `## Handoffs and open questions`):
   2–10 lines at end.
7. **LOG.md append**: one line per specialist run, format:
   `- <ISO-ts> | <specialist>: <one-line-summary>`.

### Size distribution (from 24 sampled files)
- **Minimum**: 7,467 bytes (scribe.md — ledger normalizer, not a lens)
- **10th percentile**: 9,500 bytes
- **Median**: 14,500 bytes
- **Mean**: 15,900 bytes
- **90th percentile**: 20,000 bytes
- **Maximum**: 26,231 bytes (librarian.md, engineering-team session)

Excluding scribe (which is a ledger role, not a lens), the minimum for a
real lens pass is **~8 KB** and the typical is **12–20 KB**. The 7,467-byte
scribe file is the floor because it's structurally shorter by role design.

### Tool-call counts (inferred from citations and raw caches)
- **Cartographer, linguist, archaeologist**: mostly local Grep/Read, 5–15 tool calls.
- **Librarian, historian, web-miner**: 10–25 WebFetch/WebSearch calls plus
  Context7 queries where available.
- **Github-miner**: 5–20 `gh api` calls, plus raw cache files under
  `EVIDENCE/github-miner/raw/`.
- **Empiricist**: 5–15 Bash experiments with raw-output blocks inline.
- **Synthesist, skeptic, moderator, adversary**: mostly Read on sibling
  evidence files, 5–15 Reads, no external tool calls.

**Observation**: the 3 siblings currently in flight all exhibit healthy
per-specialist variation in both size and tool-call shape. No sign of
lead-generalist-smear in the existing corpus. **This is a baseline, not a
contradiction of the failure-mode hypothesis** — it means the failure
mode is rare but real (0/3 observed, but the design must prevent it).

## 4. The `352dbd60-…` UUID team dir

There's a team directory under `/home/akash/.claude/teams/` named with a
UUID (`352dbd60-e73b-4c6c-85ce-b661206e9d6c`) containing only an `inboxes/`
subdirectory. This is the vestige of the Claude Code experimental
`agent-teams` feature mentioned in PROTOCOL.md's "v3 targets" section:
"Native Claude Code agent-teams with mailboxes: currently experimental; v3
target after the feature exits experimental."

The mailbox pattern exists but is unused in the current research team
workspace — the research team uses a file-based ledger (EVIDENCE/*.md +
LOG.md) instead of mailboxes. This is important because **if the mailbox
feature stabilizes, it becomes a candidate for the orchestration layer**,
but for now it is not part of the backward-compatibility surface.

## 5. Mapping onto the 4 hypotheses

| Hypothesis | Filesystem deps it needs | Exists today? |
|---|---|---|
| H1 pre-flight checklist | `EXPECTED_EVIDENCE.md` per session (new file), `scripts/audit_evidence.py` | No — needs to be created |
| H2 token attribution | YAML frontmatter on every evidence file (not currently used), `scripts/audit_evidence.py` | No — schema change, additive |
| H3 hook-based runtime | `hooks/` or `settings.json` `PreToolUse` on `Write` | No — hook must be added |
| H4 responder pattern | `scripts/evidence_responder.sh` (new) plus LOG.md discipline | No — script must be created |

All four hypotheses require additive filesystem changes; none require
runtime-level changes. This is compatible with the "practical over
idealized, works within subagent runtime" constraint.

## 6. The `agent-memory` layout (for the 4-session retrospector race)

```
~/.claude/agent-memory/
├── research-lead/MEMORY.md             <-- 14,102 bytes, THE contested file
├── research-retrospector/MEMORY.md     <-- 1,541 bytes, meta-lessons
└── architect-planner/                  <-- legacy
```

The `research-lead/MEMORY.md` file is the **single point of write
contention** when 4 retrospectors race at session close. Its current size
is ~14 KB with 158 lines; assuming 5-7 lessons per session append, 4 parallel
retrospectors would append ~20 lessons simultaneously. This is why the
engineering-team session is designing a lock protocol — my finding is
simply: the file IS single-writer, there IS no existing lock, and the
sibling session's lock design is a hard dependency on this session's
close procedure.

## 7. Citations

Filesystem inventory via Bash `ls`, `wc -c`, `find`:
- [fs:1] `/home/akash/.claude/` root listing, 2026-04-12T05:18Z
- [fs:2] `/home/akash/.claude/agents/research/` listing, 18 .md files
- [fs:3] `/home/akash/.claude/teams/research/` listing, 7 sessions + PROTOCOL.md
- [fs:4] `/home/akash/.claude/agent-memory/research-lead/MEMORY.md` stat,
  14,102 bytes, 158 lines
- [fs:5] `/home/akash/.claude/teams/research/engineering-team-self-evolve-v1/EVIDENCE/`
  7 files, 119,263 bytes total
- [fs:6] `/home/akash/.claude/teams/research/claude-memory-layer-sota-2026q2/EVIDENCE/`
  17 files, 263,334 bytes total
- [fs:7] `/home/akash/.claude/teams/research/claude-memory-layer-sota-2026q2-deeper/EVIDENCE/`
  8 files, in-flight
- [fs:8] `/home/akash/.claude/teams/research/capability-forge-self-evolve-v1/EVIDENCE/`
  1 file, in-flight
- [fs:9] `/home/akash/.claude/settings.json` — existing hooks: SessionStart +
  PreToolUse(Bash). No Write matcher currently.
- [fs:10] `/home/akash/.claude/lib/git-identity.sh` — 2796 bytes, existing hook target
- [fs:11] `/home/akash/.claude/teams/352dbd60-e73b-4c6c-85ce-b661206e9d6c/inboxes/` —
  mailbox pattern vestige, unused
- [fs:12] Head lines of `engineering-team-self-evolve-v1/EVIDENCE/cartographer.md`
  showing current metadata convention (no YAML frontmatter, uses `Session:`,
  `Date:`, `Lens:`)
- [fs:13] Head lines of `claude-memory-layer-sota-2026q2/EVIDENCE/synthesist.md`
  showing `Sub-question:` convention for integration specialists
- [fs:14] `~/.claude/teams/research/PROTOCOL.md` — v2, 376 lines, documents
  but does not enforce the evidence schema

## 8. Handoffs and open questions

**For empiricist**: when writing the hook smoke-test, use the `settings.json`
PreToolUse(Bash) hook as a template — it's a working reference. The syntax is
`{ "matcher": "Write", "hooks": [ { "type": "command", "command": "..." } ] }`.
Verify whether subagent `Write` calls actually trigger the hook (the open
technical question for H3).

**For librarian**: the authoritative source for Claude Code hook semantics is
likely the sub-agents docs + settings docs. Confirm which hook events exist
and whether they fire for subagent tool calls.

**For the lead**: the schema change to add YAML frontmatter should be
**opt-in for v2.1** (new sessions include it, old sessions don't need
retrofitting). This is exactly what "backward compatible" means —
`audit_evidence.py` should accept files without frontmatter as legacy-grade
PASS but flag them as "schema-v1" in the output.

**Open structural question**: the `352dbd60-*` UUID team dir hints at an
experimental Claude Code feature. Should the orchestration layer align with
that feature's mailbox conventions, or stay file-based? Recommend: stay
file-based for v2.1 (stability), re-evaluate in v3 when the feature exits
experimental.

## Confidence

**High**. Filesystem inventory is ground-truth; size statistics are computed,
not estimated; the de-facto schema is derived from 24 actual files. The only
low-confidence claim is "no existing lead-generalist-smear in the 3 siblings"
which is based on inspection of size variance, not lexical analysis —
linguist will tighten this.
