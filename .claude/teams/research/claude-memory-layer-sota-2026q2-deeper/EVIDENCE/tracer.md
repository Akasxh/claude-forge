# Tracer — runtime causal chain for Hook A scribe routing and lead lazy-load

Sub-question: walk the exact runtime path from (a) retrospector emits new lesson → scribe reads → scribe decides route → scribe writes, and (b) next session start → lead reads MEMORY.md → encounters topic-file reference → lead reads topic file. Identify every tool call, every file read/write, every decision point. The chains produce the contract the Edit diffs must satisfy.

## Method

- Read current `~/.claude/agents/research/research-scribe.md` verbatim
- Read current `~/.claude/agents/research/research-lead.md` verbatim  
- Read pilot's `EVIDENCE/tracer.md` for the v2 baseline chain
- Cross-referenced with Claude Code memory docs for tool access and auto-injection

## Chain A — Retrospector-to-topic-file routing (Hook A write path)

This is the new chain Hook A introduces. The retrospector's behavior does NOT change; only the scribe's dedup/curate behavior is extended.

```
[trigger]
  Session close. research-lead dispatches research-retrospector.
       │
       ▼
[retrospector writes raw lessons]
  research-retrospector reads the session workspace (EVIDENCE/*, SYNTHESIS.md,
  LOG.md), extracts 3-7 durable lessons, writes them in append mode to
  ~/.claude/agent-memory/research-lead/MEMORY.md (the index file).
  Each raw lesson has the standard 5-line shape:
    ### Lesson N — <name>
    - Observed in: <slug> (<date>)
    - Failure mode addressed: <MAST tag>
    - Lesson: <prose, can be long>
    - Rule of thumb: <one-liner>
    - Counter-example / bounds: <when-not-to-apply>
       │
       ▼
[scribe dispatch]
  research-lead dispatches research-scribe for dedup + curation pass.
       │
       ▼
[scribe reads]
  scribe reads:
    (a) MEMORY.md (current state, post-retrospector append)
    (b) every *.md file in ~/.claude/agent-memory/research-lead/
        EXCEPT MEMORY.md (these are existing topic files)
        — Glob pattern: ~/.claude/agent-memory/research-lead/*.md
       │
       ▼
[scribe dedup pass]
  For each new lesson in the session's append:
    1. Check semantic duplicates against existing MEMORY.md entries.
       If match → merge via the existing v2 protocol (preserve both observations,
       extend Reinforced-by list). STOP for this lesson.
    2. Check contradictions against existing entries.
       If match → mark old as Superseded by <new>; leave both. STOP for this
       lesson.
    3. Check staleness. (Existing v2 behavior, unchanged.)
       │
       ▼
[scribe routing decision — THE NEW STEP]
  For each new lesson that survived dedup:
    Apply the routing heuristic (defined below). Two possible outcomes:
      A. INDEX route (most lessons): keep the full lesson in MEMORY.md
         as-is. Nothing else to do.
      B. TOPIC route (long-tail reference artifacts): the lesson's
         reference payload (code block, table, verbatim quote, schema)
         moves to a topic file; a short stub stays in MEMORY.md.
       │
       ▼
[scribe writes on TOPIC route]
  1. Generate a topic slug: `<kebab-case-topic>.md` (e.g.
     `mempalace-fraud.md`, `latentmas-file-map.md`, `memx-ranker.md`)
  2. Write full reference payload to
     ~/.claude/agent-memory/research-lead/<topic-slug>.md
     (Edit tool with create=true flag, or Write tool)
  3. Edit MEMORY.md to replace the long lesson with a stub:
     ### Lesson N — <name>
     - Observed in: <slug> (<date>)
     - Failure mode addressed: <MAST tag>
     - Lesson: <1-2 sentence summary>
     - Rule of thumb: <one-liner>
     - See: `<topic-slug>.md` for <what's in the topic file>
  4. Append to LOG.md: `scribe-curator: routed Lesson N to topic file <slug>`
       │
       ▼
[scribe size check]
  After all routing, scribe checks MEMORY.md byte count.
  If > 25KB → mark bottom-quartile entries as Archive candidate (v2 behavior,
  unchanged; the topic-routing should have prevented this in most cases).
       │
       ▼
[chain complete]
  MEMORY.md is leaner (stubs replace verbose lessons).
  Topic files exist for the detailed content.
  LOG.md has a trail of routing decisions.
```

### The routing heuristic (adjudicated by linguist, IH-A)

The scribe routes to a topic file if AND ONLY IF **both** conditions hold:

1. **Length condition**: the lesson's full body (prose + code blocks + tables + quotes) exceeds 1,500 characters **OR** contains a code block of ≥10 lines **OR** contains a table of ≥5 rows **OR** contains a verbatim quote of ≥300 characters.
2. **Type condition**: the lesson's body contains **reference content** (code, schemas, citations, benchmark tables, verbatim quotes, file maps) — i.e., content the lead will read OCCASIONALLY (not EVERY session start).

If only condition 1 is satisfied (long lesson, but it's a long rule of thumb with no reference payload), **keep in index**. The index must stay navigational; size alone is not the trigger.

If only condition 2 is satisfied (short lesson with a small code block), **keep in index**. The reference is small enough to stay.

Both conditions → topic route.

### Concrete examples

| Lesson content | Route | Reason |
|----------------|-------|--------|
| "When user prompt is short, distrust your sub-question list to catch last 14 days" (300 chars, pure rule) | INDEX | Neither condition |
| "MemPalace fraud case study: 3 audits + maintainer ack + full reproductions" (~4KB, citations + quotes) | TOPIC | Both conditions |
| "Hook B hybrid ranker: `score = 0.45*sem + 0.25*rec + 0.05*freq + 0.10*imp`" (small code, ~200 chars total) | INDEX | Only condition 2 partially, body too small |
| "The 17 moderator verdict patterns we encountered: (table of 17 rows)" (~5KB, table) | TOPIC | Both conditions |
| "LatentMAS file map: run.py → methods/latent_mas.py → line 57 _truncate_past ..." (~2KB, reference) | TOPIC | Both conditions |
| "REUSE / EXTEND / REWRITE heuristic on reruns" (~600 chars, pure rule) | INDEX | Only condition 2 partial, mostly prose |

## Chain B — Next-session lead lazy-load (Hook A read path)

```
[trigger]
  Akash (or the main session) invokes research-lead for a new session.
       │
       ▼
[auto-injection]
  Claude Code runtime reads the first 200 lines / 25KB of
  ~/.claude/agent-memory/research-lead/MEMORY.md and injects it into the
  lead's system prompt at session start. This happens BEFORE the lead's
  first message. (Per code.claude.com/docs/en/sub-agents § "Enable
  persistent memory", verbatim: "The subagent's system prompt also
  includes the first 200 lines or 25KB of MEMORY.md in the memory
  directory, whichever comes first")
       │
       ▼
[lead reads its own system prompt]
  research-lead's Round 0 Step 3 instruction (existing): "Consult MEMORY.md"
  — now satisfied by the auto-injection.
  The injected MEMORY.md contains stubs for topic-routed lessons, each
  ending with `See: <topic-slug>.md for <what's in it>`.
       │
       ▼
[lead encounters topic reference during Round 0 or Round 1]
  As the lead drafts QUESTION.md, HYPOTHESES.md, and the dispatch plan,
  it may encounter a lesson stub that references a topic file by filename.
  Example: "Lesson N — see mempalace-fraud.md for the full audit trail".
  
  The lead decides whether the current session's topic is relevant to the
  topic file. If YES:
    1. Lead uses Read tool to open
       ~/.claude/agent-memory/research-lead/<topic-slug>.md
    2. Lead now has the detailed reference in its current context.
  If NO:
    1. Lead ignores the reference. The stub is enough for navigation.
       │
       ▼
[lazy-load signal]
  Claude Code's UI surfaces "Recalled memory: <topic-slug>.md" when the
  read happens (per docs verbatim: "When you see 'Writing memory' or
  'Recalled memory' in the Claude Code interface, Claude is actively
  updating or reading from ~/.claude/projects/<project>/memory/").
  This is observable — Akash can see when topic files are being read.
       │
       ▼
[chain complete]
  Lead has the detailed content if needed; skipped reading it if not
  relevant. Topic files stay out of the session context unless load-
  bearing.
```

### Lead persona edit requirement (derived from Chain B)

The current research-lead.md Step 3 says:

> "Consult MEMORY.md. Read `~/.claude/agent-memory/research-lead/MEMORY.md`. Check for lessons about this question class or similar past sessions. If the runtime auto-injected it, you already have it; otherwise read it yourself as Step 3."

This MUST be extended with:

> "When a MEMORY.md entry references a topic file by filename (e.g. 'See: `mempalace-fraud.md` for the full audit'), treat the reference as a lazy pointer. Read the topic file with the Read tool ONLY when the current session's subject matter overlaps with the topic file's domain. Do not preload all topic files — that defeats the index's purpose."

The exact Edit-tool diff is in `EVIDENCE/scribe-edit-plan.md`.

## Chain C — Failure modes in the routing (blast radius)

### Failure C1: scribe routes everything to topic files, index becomes empty

**Scenario**: scribe's heuristic fires too aggressively. Every new lesson gets routed. MEMORY.md becomes a list of stubs with no substantive content.

**Blast radius**: lead's session-start injection loses signal density. Lessons are still navigable (stubs point to files) but the lead has to do more file reads to get the same info.

**Mitigation**: heuristic requires BOTH length AND type conditions. Short rules stay in index even if they're "reference-y". Pure prose stays in index even if long.

**Detection**: after each session, scribe logs routing decisions to LOG.md. If >50% of new lessons are topic-routed in a single session, flag as an anomaly. (Threshold set by IH-F empirical monitoring.)

### Failure C2: scribe routes a load-bearing rule to a topic file

**Scenario**: a lesson whose rule-of-thumb matters on every session (e.g., "dispatch planner first, then wide") gets its body moved to a topic file because of a long code example. Lead sees the stub, doesn't read the topic file, misses the rule.

**Blast radius**: rule violation in the next session. Concrete harm.

**Mitigation**: the rule-of-thumb MUST stay in MEMORY.md even on topic-routed lessons. Only the reference payload moves. The stub schema includes the full rule-of-thumb line.

**Detection**: skeptic attack 3 (Hook A attack on Chain B) explicitly checks whether stubs preserve the rule.

### Failure C3: lead doesn't see the topic file because MEMORY.md doesn't reference it

**Scenario**: scribe writes a topic file but forgets to add the `See: <filename>.md` line to MEMORY.md. The topic file is orphaned.

**Blast radius**: topic file is unreachable via normal session-start flow. Only accessible if lead explicitly `ls`es the directory (which the current persona does NOT do).

**Mitigation**: scribe's write-topic-file subroutine is atomic — it must write the topic file AND update MEMORY.md in the same operation. The routing action is defined as "replace lesson body with stub in MEMORY.md + create topic file" — NOT two independent steps.

**Detection**: a post-routing audit: scribe checks that every *.md file in the directory (except MEMORY.md) is referenced by filename in MEMORY.md. If orphans exist, log a warning to LOG.md. This is a cheap self-check.

### Failure C4: specialist writes to the wrong topic file during a session

**Scenario**: during a session, a specialist (not the scribe) happens to write to `~/.claude/agent-memory/research-lead/foo.md` thinking it's a session-local file. Corrupts a cross-session topic file.

**Blast radius**: one topic file is wrong. Lead reads wrong data on next session.

**Mitigation**: specialists do NOT have write access to `~/.claude/agent-memory/research-lead/` in their persona contract. The only agents that touch this directory are research-retrospector (writes MEMORY.md appends) and research-scribe (dedup + routing). This is a persona-level invariant, enforced by convention not by FS permissions.

**Detection**: the scribe's session-start health check can hash each topic file and compare on session end. Out-of-band modification shows as a hash change. Optional; not required for MVP.

## Contract summary for the Edit-tool diffs

From these chains, the Edit diffs for scribe and lead must satisfy:

1. **Scribe routing is atomic**: topic-file write + MEMORY.md stub edit in the same routing decision. No orphans.
2. **Stub schema preserves rule-of-thumb**: only the reference payload moves to topic.
3. **Lead reads topic files lazily**: not all at once, not never. Only when current subject overlaps.
4. **LOG.md trails every routing action**: `scribe-curator: routed <slug> to topic <filename>`.
5. **Topic file naming**: kebab-case slug, .md extension, at the flat level of the agent-memory directory (NOT in a `topic/` subdirectory).
6. **Size check still runs**: the 25KB ceiling check is the backstop; topic routing is the first-line defense.

## Confidence

**High**. Every chain step cites the behaviors currently in the scribe.md and lead.md persona files (verbatim read at the top of this session) and the Claude Code memory docs (fetched 2026-04-12). No speculation about runtime behavior.

## Handoff

- **scribe-edit-plan** — uses this contract to produce the Edit tool diffs
- **linguist** — adjudicates the "condition 2" vocabulary (what counts as "reference content")
- **empiricist** — cost of the routing decision (extra Read calls at session start for topic files)
- **skeptic** — attack the 4 failure modes above; any missed?

## Citations

- research-scribe.md current version — `~/.claude/agents/research/research-scribe.md`, read 2026-04-12
- research-lead.md current version — `~/.claude/agents/research/research-lead.md`, read 2026-04-12
- Claude Code sub-agents memory docs — `code.claude.com/docs/en/sub-agents` § "Enable persistent memory", retrieved 2026-04-12
- Claude Code auto memory docs — `code.claude.com/docs/en/memory` § "How it works" and § "Storage location", retrieved 2026-04-12
- Pilot tracer.md — `~/.claude/teams/research/claude-memory-layer-sota-2026q2/EVIDENCE/tracer.md`, read 2026-04-12 (reused as baseline Chain 4)
