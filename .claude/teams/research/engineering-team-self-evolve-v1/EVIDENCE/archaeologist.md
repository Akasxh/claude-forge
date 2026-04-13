# Archaeologist — evolutionary pressure on research-team and what it means for engineering-team

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: historical, evolutionary, lessons encoded

## Method

Read `~/.claude/teams/research/PROTOCOL.md` (v2 canonical), `~/.claude/teams/research/PROTOCOL.v1.bak` (archived v1), `~/.claude/teams/research/claude-memory-layer-sota-2026q2/` (the v2 pilot), the research-lead persona file, and `~/.claude/agent-memory/research-lead/MEMORY.md` (12 lessons). The goal: understand what pressures drove v1 → v2, so v1-of-engineering starts already-encoded with those pressures rather than re-learning them.

## v1 → v2 diff (summarized from PROTOCOL.md's "What changed from v1" section)

v1 was a 12-specialist flat team with a lead that dispatched, arbitrated, and synthesized. Five hard failures were observed or predicted from the MAST literature and the Anthropic post, and v2 added five specialists to close those gaps:

1. **`research-planner`** added — closes FM-1.1 (disobey task specification via over/under-dispatch). v1 let the lead decide dispatch breadth from intuition; v2 forces the planner to write a dispatch recommendation as Round 0 output, which the lead may override but must justify. The Anthropic post's #1 cited failure is "50 subagents for simple queries," which v1 had no defense against.

2. **`research-adversary`** added — closes FM-3.3 (incorrect verification) on the corpus-capture variant. v1 had a skeptic but not an adversary. Anthropic's own failure list includes "choosing SEO-optimized content farms over authoritative sources," which the skeptic (attacking the synthesis from inside) literally cannot see.

3. **`research-moderator`** added — closes FM-2.5 (ignored other agent's input). v1 let the lead arbitrate contradictions. The lead is ALSO the synthesizer, therefore has confirmation-bias stake in the arbitration outcome. Claude Code's agent-teams docs explicitly recommend debate-structured investigation for contradictions.

4. **`research-evaluator`** added — closes FM-3.1 (premature termination) and FM-3.2 (incomplete verification). v1 closed confidence claims on the lead's own say-so. v2 forces a separate 5-dim rubric pass (Anthropic's published rubric) before "high confidence" can be stamped.

5. **`research-retrospector`** added — closes the cross-session learning gap. v1 restarted from zero every session. v2 implements the ACE (arxiv 2510.04618) "generator/reflector/curator" playbook pattern with retrospector as reflector, scribe as curator, MEMORY.md as playbook.

Plus **frontmatter hardening**: `effort: max` added to every specialist so runtime enforces the "all Opus max effort" doctrine. Plus **adopted-persona pattern 2**: v2 made explicit that when research-lead is invoked as a subagent (not as a main thread), it executes specialist methods directly rather than sub-dispatching, because subagents cannot spawn subagents.

## Lessons the pilot session added (MEMORY.md 8-12, from claude-memory-layer-sota-2026q2)

The v2 pilot produced 5 fresh lessons after running a real session, bringing MEMORY.md from 7 starter lessons to 12. Each is evolutionary pressure to bake into engineering-team:

**Lesson 8 (MEMORY.md line 126-131)**: "When the user prompt is short, distrust your initial sub-question list to catch the latest 14 days." Memory-layer v1 missed Latent Briefing, MemPalace, MAGMA, EverMemOS, and the 47-author taxonomy paper. **Pressure for engineering-team**: the engineering-planner must include "what shipped in the last 14 days" as a structural sub-question for any topic producing weekly arxiv output. SWE-bench agents are exactly that kind of topic in 2026.

**Lesson 9 (MEMORY.md line 133-138)**: "Adversary catches what skeptic cannot: corpus-level fraud." MemPalace case study: 21K stars in a week, 1.5M X views, 96.6% benchmark claim that measured ChromaDB not MemPalace. Three independent audits exposed; maintainer acknowledged. **Pressure for engineering-team**: engineering-adversary must run pre-emptively on any session where the research input cites benchmark numbers. SWE-bench-verified scores are known-contested. Devin's published numbers have been challenged on X. Cursor's benchmarks are mixed. The adversary gate is not optional.

**Lesson 10 (MEMORY.md line 140-144)**: "REFRAME is a valid moderator verdict — don't force winner-take-all on mis-posed debates." C4 debate in memory-layer session: "is Claude Code's existing memory mechanism insufficient?" The right verdict was REFRAME to "what cells of the taxonomy are uncovered," not A_WINS or B_WINS. **Pressure for engineering-team**: engineering-moderator must inherit the 5-verdict set `{A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER}`. The plan-vs-ReAct debate in this very session is likely a REFRAME ("not mutually exclusive — H3's two-phase design uses both in different scopes").

**Lesson 11 (MEMORY.md line 146-151)**: "Reuse v1 evidence on rerun; append addenda, don't rewrite." Memory-layer v2 relaunch reused planner, librarian, historian, web-miner, github-miner raw cache; added historian-addendum.md. Saved ~20 tool calls. **Pressure for engineering-team**: when a failed verifier triggers re-dispatch, the engineering-lead must classify existing files as REUSE / EXTEND / REWRITE. Code is more brittle than research — a REWRITE may actually mean "revert and retry" rather than "modify in place." But the category-discipline applies.

**Lesson 12 (MEMORY.md line 153-158)**: "REPORTED-NOT-VERIFIED is a valid evidence tier on paywalled / unreachable primaries." Ramp Labs Latent Briefing returned 402; direction triangulated by LatentMAS + LRAgent + MemOS. Numbers marked REPORTED-NOT-VERIFIED, used as direction not magnitude. **Pressure for engineering-team**: when the research SYNTHESIS feeding the engineering session contains REPORTED-NOT-VERIFIED claims, engineering-executor must BE AWARE of them — if the plan depends on a specific number from a paywalled source, engineering-architect must empirically verify before executor commits to that number. This is the handback loop's first protocol.

## What v2 still doesn't have that Anthropic's own system does

The research PROTOCOL's "v3 targets" section (lines 151-155) lists three gaps:

1. **Asynchronous dispatch**. v2 is synchronous within a round. Anthropic's own system async-dispatches subagents and collects returns. For engineering-team v1: same synchronous limitation, because Claude Code's runtime doesn't expose async subagent dispatch primitives as of April 2026. The parallel-instance concurrency protocol is a separate concern.

2. **Native Claude Code agent-teams with mailboxes**. Currently experimental per the docs. v1 engineering-team uses files-on-disk, not mailboxes. Future v2 engineering-team may be able to migrate.

3. **Tool-description self-rewrite** (Anthropic reports 40% task-time reduction). v2 writes *lessons* to MEMORY.md; Anthropic writes *tool description patches* that the runtime applies. v1 engineering-team keeps the lesson-patch pattern (simpler, inspectable); a future version may add runtime tool-description editing.

## Pilot session meta-stats (from claude-memory-layer-sota-2026q2/LOG.md and SYNTHESIS.md)

Observable from the workspace:
- 16 evidence files (planner, cartographer, archaeologist, librarian, tracer, empiricist, skeptic, adversary, historian, historian-addendum, linguist, web-miner, github-miner subdirectory, synthesist, moderator, evaluator, retrospector, scribe)
- 5 moderator debates (load-bearing contradictions)
- Confidence: HIGH on architecture, MEDIUM on Hook C numbers (paywalled primary)
- Evaluator PASS on all 5 rubric dimensions
- Retrospector extracted 5 lessons to MEMORY.md (lessons 8-12 above)
- Session relaunched once (v1 → v2) to catch the 14-day freshness gap

The pilot validated: the gate ordering (planner → wide → synthesist → moderator → skeptic → adversary → evaluator → retrospector) holds; the file-backed ledger survives multi-round iteration; the adversary gate produced material corrections that the skeptic missed; and the REFRAME verdict was the highest-value moderator output of the session.

**Finding**: **the v2 protocol is battle-tested once**. Engineering-team v1 can adopt it with high confidence on the structural pattern.

## Evolutionary pressures that should carry over to engineering-team-v1

1. **Adversarial gates are the differentiator**. Without the five v2 additions (planner, adversary, moderator, evaluator, retrospector), the team degenerates to v1-level "dispatch + eyeball." Engineering-team must have **all five analogues**, not a subset.

2. **Frontmatter enforcement is load-bearing**. Every specialist's `model: opus` + `effort: max` is what prevents silent downgrade under pressure. Engineering-team inherits this verbatim.

3. **Files are the memory**. Research-team v2 uses files-on-disk for everything that needs to survive beyond a single thread's context window. Engineering-team inherits this — in fact, engineering needs it MORE because code changes persist and need audit trails.

4. **Adopted-persona pattern 2 is the fallback execution model**. When engineering-lead is invoked as a subagent (as research-lead is in this very session), it cannot sub-dispatch. Must read specialist files as behavioral contracts. Document in engineering-lead persona and in PROTOCOL.md.

5. **MEMORY.md lesson 8-12 apply as if observed here**. Engineering-team inherits the 14-day freshness sweep pattern, the adversary mandate on benchmark claims, the REFRAME moderator verdict, the REUSE/EXTEND/REWRITE classification on re-dispatches, and the REPORTED-NOT-VERIFIED evidence tier — because these are cross-session lessons, not domain-specific to research.

## Evolutionary pressures that are engineering-specific (and NEW)

Research-team v2 didn't have to deal with:

1. **Code persistence**. Evidence files in research are consumed-and-forgotten. Code changes persist in the user's working tree forever (until committed or reverted). An "incorrect verification" in engineering means a bug shipped. Engineering-verifier + engineering-reviewer are on the critical path in a way research-evaluator is not.

2. **Test execution non-determinism**. Engineering sessions run tests. Tests can flake. Research-empiricist runs experiments but research is less sensitive to test ordering than engineering is. Engineering-verifier needs flake-detection awareness.

3. **Rollback semantics**. If engineering-executor breaks something, can we back out? Research has no rollback — you read the wrong file, you just read the right file next. Engineering needs a git snapshot before each executor pass, and a rollback protocol if verifier fails.

4. **Cross-team handoff from research SYNTHESIS.md as binding spec**. Research sessions stand alone. Engineering sessions are usually downstream of a research session. The handoff contract is new.

5. **Parallel-instance concurrency on MEMORY.md**. Research v2's MEMORY.md write is at session close (single writer per session), but two sessions can still race. Engineering adds a second population of writers to the same file. The segregation protocol is a NEW structural concern that v2 didn't address.

## Historical artifact: v1 PROTOCOL backup

`~/.claude/teams/research/PROTOCOL.v1.bak` exists. I did not read it in full — v2's PROTOCOL.md already documents the diff. Its existence is itself a lesson: **keep PROTOCOL versions in backup so later sessions can archaeology the rationale**. Engineering-team should do the same: `~/.claude/teams/engineering/PROTOCOL.md` initially, backup to `PROTOCOL.v0.bak` on first update.

## Handoff note to synthesist

Five cross-session lessons (MEMORY.md 8-12) must be cited in SYNTHESIS.md's "Inherited pressures" section. They are load-bearing for the final design. The synthesist does not need to re-derive them — they are already published playbook, not new findings.

## Confidence in my archaeology

**HIGH** — the PROTOCOL.md, the pilot session workspace, and MEMORY.md are all directly readable with full trace. No interpretation required; the v1→v2 pressure is self-documented by the v2 authors (the research team itself). Only medium-confidence note: the V1 PROTOCOL backup was not opened, so if there are undocumented v1 failures, those are invisible. The synthesist should not depend on "v1 didn't have failure X" unless the PROTOCOL.md's own "what changed" list names X.
