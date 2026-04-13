# HYPOTHESES.md — deeper round (implementation-grade)

**Seeded by**: research-lead at Round 0, before dispatching specialists.
The pilot's strategic hypotheses are already resolved (see pilot EVIDENCE/
skeptic.md § "Hypothesis status update"). This round's hypotheses target
the implementation-grade choices.

---

## IH-A — Scribe routing heuristic: LENGTH + TYPE, not LENGTH alone

**Claim**: The scribe's "route to topic file" decision is best triggered by
a combined predicate: the new entry contains long-form content (code block
>= 10 lines, verbatim quote >= 200 chars, table >= 5 rows) OR the entry
is clearly a reference artifact (a citation, a file-map, a benchmark table,
a schema) rather than a rule of thumb. Pure rules of thumb always stay in
MEMORY.md even if long.

**Differentiator**: rejects the naive "if > N bytes move it out" rule. The
25KB ceiling is on the index, but the index must also remain HIGH-SIGNAL,
not just SHORT.

**Falsifiable by**: a test case where a long-but-rule-of-thumb lesson ends
up in a topic file despite the content being navigational — that's a miss.

**Status**: open, adjudicated by linguist + skeptic.

---

## IH-B — MCP language: Python wins for this MCP specifically

**Claim**: Python wins over Node for `~/.claude/memory-mcp/` because (a)
`sqlite-vec` has a first-class Python wheel, (b) stdlib `sqlite3` includes
FTS5 on modern builds, (c) Akash's ML toolchain is Python-native so
sentence-transformers / embeddings pipelines are one import away, (d) the
MCP Python SDK (`mcp` on PyPI) is now stable and production-grade as of
2026. Node's advantage (faster startup, native async) doesn't matter for
a process that serves a single developer's local session.

**Differentiator**: this is an infrastructure choice, not a philosophical
one. The test is "what's the single easiest way to ship FTS5 + vector +
MCP with maximum reuse of Akash's existing skill set."

**Falsifiable by**: if Python MCP SDK has significant stability issues or
sqlite-vec's Python bindings are broken on his platform. Librarian confirms
via Context7 + PyPI + upstream repo.

**Status**: open, adjudicated by librarian + github-miner + empiricist.

---

## IH-C — LatentMAS spike is a one-evening file-map + hello-world, NOT a full cross-specialist integration

**Claim**: The one-evening Hook C spike's correct scope is (1) clone
Gen-Verse/LatentMAS if it exists, (2) identify the compact-then-attend
function(s) and write a FILE_MAP.md, (3) run a minimal example with vLLM
serving Qwen-14B and observe KV cache prefix hit rate. It does NOT integrate
with research-lead's dispatch loop — that's a separate week-level project
for the forthcoming Engineering Team.

**Differentiator**: the pilot's SYNTHESIS says "time-box to one evening"
but doesn't specify scope. An unbounded "integrate latent briefing" scope
would blow the time box immediately. Naming the minimal spike keeps the
time box honest.

**Falsifiable by**: if Gen-Verse/LatentMAS doesn't actually exist or is
a stub repo, the spike scope changes to "write a from-scratch vLLM prefix-
caching demo" which has different shape (empiricist must verify).

**Status**: open, adjudicated by github-miner + empiricist + skeptic.

---

## IH-D — Parametric LoRA distillation is deferred until MEMORY.md has 30+ REINFORCED lessons

**Claim**: The minimum dataset size to justify LoRA distillation is NOT
the raw lesson count. It's the count of lessons that have been REINFORCED
across ≥3 sessions OR ≥30 days. Lessons that have never been reused are
too unstable for weight-baking. Current MEMORY.md has ~10 lessons;
maybe 4-5 are stable enough to distill. The decay gate "reinforced by N,
stable over M days" is the load-bearing filter, not the total count.

**Differentiator**: rejects "distill when MEMORY.md hits 25KB" (which is
a size-based trigger that ignores stability). The stability signal is a
cross-session reinforcement pattern the scribe tracks in the "Reinforced
by" field.

**Falsifiable by**: if a distilled LoRA trained on <30 stable lessons
still gives measurable capability lift on an honest eval. Empiricist
must measure.

**Status**: open, adjudicated by empiricist + historian (prior art on
minimal LoRA dataset sizes) + skeptic.

---

## IH-E — The 0-14 day fresh sweep finds nothing that invalidates the plan

**Claim**: The pilot was run at cutoff 2026-04-12. The deeper round is the
same day. The 0-14 day sweep will find incremental releases (Mem0 patches,
Letta PRs) but nothing that invalidates the 4-phase architecture because
the architecture is grounded in peer-reviewed primaries (ACE, HippoRAG 2,
LatentMAS, MemX) that don't shift week-to-week. The adversary's job is
nonetheless to verify this, not to assume it.

**Differentiator**: pilot lesson 8 says "don't trust your initial list to
catch the latest 14 days." Deeper-round corollary: "run the sweep AGAIN
specifically to check whether the pilot itself missed something."

**Falsifiable by**: if the sweep finds a paper or project that genuinely
invalidates Hook A, B, C, or parametric direction. The addendum gets
written if so; the synthesis gets amended if so.

**Status**: open, adjudicated by adversary + historian + web-miner +
github-miner.

---

## IH-F — The right owner for Hook B's "is Hook A insufficient" metric is empiricist, not lead

**Claim**: The metric that triggers Hook B is empirical, not editorial.
Specifically: over 10 research sessions, how many times did a specialist
fail to find a topic file that existed in `~/.claude/agent-memory/
research-lead/topic/`? If >20%, Hook B is warranted. If <5%, Hook A is
sufficient and Hook B is a waste. The metric runs continuously in the
background without Akash having to audit sessions manually.

**Differentiator**: rejects "Akash eyeballs whether it feels slow." The
empirical criterion decouples the build decision from his mood.

**Falsifiable by**: if the metric is too expensive or too noisy to
maintain. Empiricist scopes the instrumentation cost.

**Status**: open, adjudicated by empiricist + tracer.

---

## Differential predictions

| Hypothesis | If TRUE, we'd observe |
|---|---|
| IH-A (length + type) | Test case with long rule-of-thumb correctly stays in index; long reference artifact correctly moves to topic file |
| IH-B (Python) | sqlite-vec Python wheel available; MCP Python SDK stable on 2026-04-12 |
| IH-C (minimal spike) | LatentMAS repo exists with identifiable compact-then-attend function; hello-world runnable in 1-2 hours |
| IH-D (stable lessons only) | Current MEMORY.md has 4-5 lessons with "Reinforced by" >= 2; total session count to 30 stable lessons is ~6 months |
| IH-E (nothing invalidates) | Sweep produces ≤2 minor releases and 0 new primary papers between 2026-04-02 and 2026-04-12 |
| IH-F (empirical trigger) | A `topic-file-miss-rate` counter is cheap to instrument (scribe logs miss events) |

## What we're NOT assuming yet

- That the pilot's 4-phase plan is 100% right. The deeper-round skeptic
  attacks it fresh to see if there's a new angle missed.
- That Python is always correct. IH-B is open; librarian verifies.
- That the LatentMAS repo exists. IH-C hinges on github-miner checking.
- That the LoRA direction is actionable this quarter. IH-D defers it
  until reinforcement data exists.
