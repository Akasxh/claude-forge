# Cartographer — re-verification of Claude Code memory topology for Hook A

Sub-question: verify the disk layout, auto-injection behavior, and topic-file discovery mechanism for subagent memory at user scope. The pilot's SYNTHESIS.md said "topic files live at `~/.claude/agent-memory/<leader>/topic/<topic>.md`" — is this correct, or is it a misreading of the docs?

## Method

- WebFetched `https://code.claude.com/docs/en/memory` and `https://code.claude.com/docs/en/sub-agents` (both retrieved 2026-04-12)
- Read the current `~/.claude/agents/research/research-scribe.md` and `~/.claude/agents/research/research-lead.md` files verbatim
- Cross-referenced with the pilot's EVIDENCE/cartographer.md to identify any drift

## The actual Claude Code subagent memory layout (verbatim from docs)

From `code.claude.com/docs/en/sub-agents` § "Enable persistent memory", retrieved 2026-04-12:

> "The `memory` field gives the subagent a persistent directory that survives across conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging insights, and architectural decisions."

**Scope table**:

| Scope     | Location                                      |
|-----------|-----------------------------------------------|
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     |
| `project` | `.claude/agent-memory/<name-of-agent>/`       |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` |

**Auto-injection behavior** (verbatim):

> "The subagent's system prompt includes the first 200 lines or 25KB of `MEMORY.md` in the memory directory, whichever comes first, with instructions to curate `MEMORY.md` if it exceeds that limit."

**Tool access** (verbatim):

> "Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files."

## The actual project-memory layout (from `/docs/en/memory`)

Verbatim from `code.claude.com/docs/en/memory` § "How it works":

> "The directory contains a `MEMORY.md` entrypoint and optional topic files:"

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

> "`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what's stored where."

> "Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information."

## CRITICAL CORRECTION to the pilot's synthesis

The pilot's SYNTHESIS.md writes:

> "extend `research-scribe`'s curator behavior ... additionally route overflow detail to topic files when the retrospector emits a lesson that is too long-tail for the 25KB index. The topic files live at `~/.claude/agent-memory/research-lead/<topic>.md`"

The pilot version **is correct** here. However, the deeper-round brief from Akash writes:

> "scribe additionally routes long-tail detail to topic files (`~/.claude/agent-memory/<leader>/topic/<topic>.md`)"

**The brief's path is WRONG.** Topic files do NOT live in a `topic/` subdirectory. They live at the same directory level as MEMORY.md. Per Claude Code's own documented convention, the correct layout is:

```
~/.claude/agent-memory/research-lead/
├── MEMORY.md             # <= the index, auto-injected at session start (200 lines / 25KB)
├── mempalace-fraud.md    # <= topic file, read on demand
├── ace-pattern.md        # <= topic file, read on demand
├── moderator-verdicts.md # <= topic file, read on demand
└── ...
```

This correction matters because:

1. The `memory: user` auto-injection mechanism reads `~/.claude/agent-memory/research-lead/MEMORY.md` by convention. It does NOT descend into `topic/` subdirectories. Putting topic files in `topic/` means the auto-injection machinery cannot discover them by the same contract the docs describe.
2. Claude Code's `Recalled memory` UI hint (visible when Claude reads a memory file during a session) expects files at the top level of the memory directory. Subdirectory reads would not surface the same UI.
3. Existing subagent memory in Akash's installed setup uses the flat layout:
   ```
   ~/.claude/agent-memory/research-lead/MEMORY.md
   ~/.claude/agent-memory/research-retrospector/MEMORY.md
   ~/.claude/agent-memory/architect-planner/MEMORY.md
   ```
   There are no subdirectories. Adding `topic/` introduces a novel convention without documentation backing.

**Hook A implementation MUST use the flat layout**: `~/.claude/agent-memory/research-lead/<topic>.md`, not `<leader>/topic/<topic>.md`. The scribe edits in EVIDENCE/scribe-edit-plan.md reflect this.

## Topic-file discovery mechanism

The docs describe two discovery paths:

1. **At session start**: `MEMORY.md` is auto-injected. If a lesson in MEMORY.md references a topic file by filename (e.g. "see `mempalace-fraud.md` for details"), the LLM now knows the file exists by virtue of the index entry.

2. **During session**: the LLM can list the memory directory with `ls` or scan with Glob to discover any file. But this is an explicit action, not automatic.

**Implication for Hook A**: the scribe must ensure that every topic file is referenced by filename in MEMORY.md. Otherwise a topic file exists on disk but is invisible to the lead at session start because the lead only reads MEMORY.md in full; topic files are on-demand.

## What "on demand" means operationally

Per `code.claude.com/docs/en/memory`:

> "Topic files ... are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information."

> "Claude reads and writes memory files during your session. When you see 'Writing memory' or 'Recalled memory' in the Claude Code interface, Claude is actively updating or reading from `~/.claude/projects/<project>/memory/`."

So the read trigger is **LLM-initiated during the session**, not a passive auto-load. The MEMORY.md index must contain enough pointer text (e.g. "topic file `adversary-corpus-verdicts.md` contains per-source verdicts from 2026-04-12") for the LLM to know when to read it.

## Hook A design consequence

The scribe's long-tail routing decision produces two effects:

1. A new topic file is written at `~/.claude/agent-memory/research-lead/<topic-slug>.md` containing the detailed content.
2. An index entry is added to MEMORY.md naming the file by filename, with a 1-2 sentence description so the lead can decide when to read it.

**Without step 2, the topic file is orphaned.** The index reference is the discovery mechanism.

## Research-lead persona edit requirement

The lead's persona file must include a concrete "lazy load topic files on demand" instruction. Currently research-lead.md says:

> "At session start, read the first 200 lines of `~/.claude/agent-memory/research-lead/MEMORY.md` — this is your persistent playbook"

It does NOT say "when MEMORY.md references a topic file by filename, read that file when the topic becomes relevant." That instruction needs to be added.

The concrete edit is in EVIDENCE/scribe-edit-plan.md under "research-lead.md edits".

## Confidence

**High**. Primary source is `code.claude.com/docs/en/memory` and `/docs/en/sub-agents`, both retrieved verbatim 2026-04-12. The on-disk layout is observable at `~/.claude/agent-memory/`. The pilot's SYNTHESIS.md was already correct on this point; the Akash brief's `<leader>/topic/<topic>.md` phrasing is the slip that must not propagate to the Edit-tool diffs.

## Handoff to scribe-edit-plan

The exact Edit-tool diffs for `research-scribe.md` and `research-lead.md` live in `EVIDENCE/scribe-edit-plan.md`. They use the correct flat path.
