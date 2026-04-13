# Skeptic — attacks on the deeper round's leading recommendation

The leading recommendation (post-moderator):
1. Hook A: exact scribe + lead edits with `AND` predicate at length 1500, AKL frontmatter optional
2. Hook B: Python MCP server with MemX default weights + per-factor logging
3. Hook C: one-evening LatentMAS spike on GSM8K-20 with go/no-go ratios
4. Parametric: 6-month-to-year-long direction, gated on ~300 stable lessons

I attack from the inside — what's silently dismissed, what's the strongest counter-hypothesis, what would make this wrong?

## Attack 1 — "Just adopt ByteRover CLI instead of building Hook A"

**The unstated assumption**: the pilot's recommendation preserves Akash's existing scribe/retrospector/lead trio because it works. But ByteRover CLI does the SAME JOB (LLM-curated hierarchical file-based memory, MCP-compatible, Claude Code integration, 4.4K stars, production-grade), ships today, and is installable with one command.

**The strongest counter-claim**: Akash could `curl -fsSL https://byterover.dev/install.sh | sh`, configure it to use his `~/.claude/agent-memory/research-lead/` directory, and get the entire Hook A + Hook B stack for free. No scribe edits, no Python MCP server, no maintenance.

**Why I might be wrong**:

1. **License**: ByteRover is **Elastic License 2.0**, not Apache/MIT. ELv2 prohibits offering the software as a hosted service to third parties. Akash is a solo user, not a service provider, so this doesn't legally block adoption — but it signals that ByteRover is a commercial-source-available product, not OSS. Akash's stack (CLAUDE.md, his custom agents, his research team) is wholly OSS-compatible. Adopting ELv2 into the stack introduces a mixed-license surface.

2. **Architecture delta**: ByteRover uses `<project>/.brv/context-tree/<domain>/<topic>/<entry>.md` (project-scoped + nested). Akash's existing setup uses `~/.claude/agent-memory/<agent>/<topic>.md` (user-scoped + flat). To adopt ByteRover, he has to either:
   - Migrate all existing agent-memory to ByteRover's layout (destroys session history)
   - Run both systems in parallel (double bookkeeping, defeats the point)
   - Symlink one to the other (fragile, breaks ByteRover's DB indexing)

3. **Agent persona integration**: ByteRover's curation is triggered by `/curate` and `/query` slash commands in the coding agent's UI. Akash's workflow is end-of-session retrospector/scribe dispatch, which is a different control flow — automated vs manual.

4. **The scribe IS already a "curator"**. Akash has an ACE-pattern reflector/curator pair (retrospector + scribe) that predates ByteRover, uses the same files-as-memory pattern, and integrates cleanly with his Research Team protocol. Replacing two working agents with a third-party CLI is a net loss in operational maturity and a bet on ByteRover's maintenance.

5. **ByteRover's 5-tier retrieval needs an LLM**. Tiers 3 and 4 require LLM calls (optimized single-call and full agentic loop) with published latencies of 5 seconds and 8-15 seconds. Akash's current topic-file-read latency is ~50ms. For the common case (Hook A path), ByteRover is **orders of magnitude slower** because it always runs through its progressive tier selection.

**Counter to my own attack**: fair points, but what if ByteRover's AKL + maturity tiers + RANKER are ALL load-bearing and Hook A without them is incomplete? Answer: Hook A adopts the AKL formula and frontmatter schema verbatim (per scribe-edit-plan Edit 1.3). The 5-tier retrieval is Hook B's job, not Hook A's. The parts of ByteRover that matter are borrowed as specs; the parts that don't matter (5-tier engine, CLI UI, DB indexer) are skipped. This is the correct level of borrowing.

**Recommendation correction**: SYNTHESIS.md should explicitly state "ByteRover is NOT adopted; ByteRover's AKL formula and frontmatter schema ARE adopted, cited to arxiv 2604.01599 § 3.2.3 + § Appendix C." This makes the borrowing explicit rather than implicit, and preserves the adversary's right to verify that the borrowed specs are honestly cited.

## Attack 2 — "The trigger metric is wrong: miss_rate over 10 sessions is too noisy"

**The unstated assumption**: 10 sessions produce enough data points to distinguish 5% from 20% miss rate with statistical confidence.

**The strongest counter-claim**: if Akash runs 2-3 research sessions per week, 10 sessions = 3-5 weeks of data. In that window, the count of RELEVANT topic files per session is ~0-3 (per empiricist's own estimate). So over 10 sessions, total relevant = 0-30. A miss rate of 20% on 15 events = 3 misses. Is 3 misses over 5 weeks a statistically distinguishable signal from 1 miss? Not really — the standard error on a binomial with n=15 is huge.

**Why I might be wrong**: the trigger metric isn't a hypothesis test; it's a practical decision aid. If the scribe logs a clear pattern (topic files that the lead SHOULD have read but didn't), the human (Akash) can eyeball it. The 20% threshold is a conversation starter, not a p-value. Moreover, the counter-hypothesis assumes all sessions have 3 relevant topic files — many will have 0, which doesn't count toward the metric at all.

**Counter to my own attack**: the metric should measure MISS EVENTS per session, not average rate. Specifically: in the last 10 sessions, how many DISTINCT topic files were judged relevant but not cited? If the answer is ≥3 distinct files (3 orphan topics over 3-5 weeks), that's a real signal of navigational failure. If ≤1, Hook A is sufficient.

**Recommendation correction**: change the trigger metric from "miss_rate > 20%" to "cumulative distinct miss-events ≥ 3 over the last 10 sessions". This is simpler to compute and more robust to small samples.

## Attack 3 — "Hook A fails silently if the scribe doesn't dispatch at session close"

**The unstated assumption**: the retrospector always runs at session close, and the scribe always runs after the retrospector. If either skips, new lessons never get routed, topic files don't get created, and the whole Hook A pipeline is a no-op.

**The strongest counter-claim**: looking at the pilot's LOG.md, the scribe sometimes runs at session START for ledger normalization but not always at session END for curation. The retrospector runs at session close by protocol but not every session runs the full close protocol (e.g., if a session is interrupted, Akash may never trigger the post-session gates).

**Why I might be wrong**: the lead's research-lead.md explicitly lists Step 17 "Dispatch research-retrospector" and Step 18 "Dispatch research-scribe" as the session close steps. The protocol is documented. If the steps are skipped, that's a process violation, not a Hook A design flaw.

**Counter to my own attack**: process violations ARE Hook A design flaws if the design doesn't tolerate them. The scribe's session-start ledger normalization should ALSO run the topic-file routing pass on any un-routed lessons found in MEMORY.md. That way, a missed session close gets recovered the next session.

**Recommendation correction**: in the scribe's session-start routine, after the standard ledger skeleton creation, run a catch-up routing pass: "read MEMORY.md; for any lesson added since the last scribe-curator LOG entry (check timestamp); apply the routing predicate; route if needed." This is a cheap idempotent fixup.

This is a genuine Edit-diff addition to `research-scribe.md` § "Method" step 1. **Add to scribe-edit-plan.md as Edit 1.5**.

## Attack 4 — "Hook B's MVP ships without an embedder warm-up, causing first-query latency spikes"

**The unstated assumption**: the `sentence-transformers` call for Qwen3-Embedding-0.6B is fast enough that lazy init is fine.

**The strongest counter-claim**: loading Qwen3-Embedding-0.6B from HuggingFace cache takes 5-15 seconds (model download + tokenizer + weights + torch compile). The first `memory.search` call of a session will stall for 5-15 seconds. For a developer who expects sub-second tool calls, this is a UX regression.

**Why I might be wrong**: lazy init is correct because eager init delays MCP startup and blocks Claude Code's session start. Akash can tolerate a one-time 10-second delay on the first query.

**Counter to my own attack**: the MVP should include a **warm-up trigger** in the server's handshake. When the MCP protocol handshake completes, the server spawns a background thread that loads the embedder WITHOUT blocking the handshake response. The first `memory.search` then either hits the warm cache (fast) or waits on the warm-up (still correct).

**Recommendation correction**: add to mcp-scaffold.md: "in `server.py`'s `__main__`, spawn a `threading.Thread(target=_get_embedder, daemon=True).start()` after `mcp.run()` is scheduled. This warms the embedder in the background. First query has its best chance of being fast."

## Attack 5 — "SFT is not the right format for distillation; DPO with synthetic negatives is"

**The unstated assumption**: supervised fine-tuning with synthetic paraphrased prompts is the right way to distill lessons into weights.

**The strongest counter-claim**: DPO (Direct Preference Optimization) trains on preference pairs: a "chosen" response (follows the rule) and a "rejected" response (violates the rule). For a playbook like Akash's, DPO directly encodes "do this, not that" — which IS what the lessons describe. SFT only sees "do this" and has no explicit signal for "not that."

**Why I might be wrong**: DPO requires a reward model OR pairwise preference data. Akash doesn't have either. The "rejected" half would have to be synthesized too (e.g., "correct: dispatch moderator. wrong: lead arbitrates."), and the synthesis cost doubles. The preference step also requires a working reward model, which is another training run.

Also: the pilot's lessons mostly DON'T have a clean wrong-answer space. For Lesson 8 ("14-day sweep on fast-moving topics"), the "wrong" answer is "skip the sweep", but there's no principled way to generate a rejection that isn't trivial to discriminate from the chosen.

**Counter to my own attack**: for the FIRST distillation pass, SFT is correct. DPO is a potential upgrade for a later pass once the first LoRA is deployed and Akash collects real preference data (e.g., "in this session, the LoRA produced output X but the correct answer was Y"). DPO is v2 of parametric, not v1.

**Recommendation**: SFT for the MVP parametric run. Mention DPO as a v2 upgrade in `parametric-spec.md`.

## Attack 6 — "The 14-day sweep is insufficient: agent memory is publishing weekly, not biweekly"

**The unstated assumption**: a 14-day window catches the relevant new work.

**The strongest counter-claim**: the pilot sweep found 4 new arxiv papers in 10 days (Apr 2, 2, 6, 8). At that rate, the next 10 days (Apr 12-22) will also produce 3-5 new papers. Akash's plan may be out of date by the time he STARTS implementing Hook A.

**Why I might be wrong**: the rate of publication ≠ the rate of relevant invalidation. Of the 4 papers found, only 1 (ByteRover) had material impact; the others corroborated but didn't refine. At a ~25% material-impact rate, the next 10 days might yield 1 material paper — significant but not blocking.

**Counter to my own attack**: the right mitigation is a **continuous sweep**, not a one-time check. Specifically: the retrospector (or a new meta-agent) should run a 7-day sweep at the START of every research session on a fast-moving topic, and inject any material findings into the session's framing. This is a v2 protocol enhancement, not a Hook A/B/C change.

**Recommendation**: file a lesson about "continuous sweep vs point-in-time sweep" for the retrospector. Do not block the current deliverables on it.

## Attack 7 — "Hook A routes the wrong class of content: benchmark tables should stay in the index"

**The unstated assumption**: benchmark tables (≥5 rows) belong in topic files.

**The strongest counter-claim**: a benchmark table in the index is EXACTLY the kind of content the lead needs every session — when dispatching empiricist or making cost decisions, a quick glance at the current benchmark landscape is load-bearing. Moving it to a topic file forces a Read call every time.

**Why I might be wrong**: benchmark tables are typically reference content that gets consulted occasionally, not every session. If a table IS load-bearing, the lesson's rule-of-thumb captures the essence ("Mem0 is MIXED on LoCoMo, do not cite as SOTA") and the full table is consultative only.

**Counter to my own attack**: the `AND` predicate + `has_table(≥5 rows)` is too aggressive. A 5-row table is often small enough to keep in the index. Raise the threshold to `has_table(≥10 rows)` to only route truly long tables.

**Recommendation correction**: in `linguist.md` and `scribe-edit-plan.md` Edit 1.2, change `contains_table(lesson.body, min_rows=5)` to `contains_table(lesson.body, min_rows=10)`. Five rows is the baseline of a summary table — too short to warrant routing.

## Hypothesis status update (after skeptic pass)

| H | Status | Skeptic verdict |
|---|--------|-----------------|
| IH-A (length AND type) | SUPPORTED with threshold correction | `AND` holds, but `has_table` threshold raises to 10 rows |
| IH-B (Python wins) | SUPPORTED | No change |
| IH-C (one-evening LatentMAS spike) | SUPPORTED | No change |
| IH-D (stable lessons only for LoRA) | SUPPORTED with DPO-for-v2 note | SFT for MVP, DPO later |
| IH-E (14-day sweep finds nothing invalidating) | SUPPORTED but weak | ByteRover refinement is material; continuous sweep is a v2 protocol item |
| IH-F (empirical trigger for Hook B) | SUPPORTED with metric refinement | Change metric to "distinct miss events ≥3 over 10 sessions" |

## What the synthesis must add (per skeptic)

1. **Explicit ByteRover handling**: "NOT adopted; AKL formula and frontmatter schema ARE adopted with citation" (Attack 1)
2. **Revised Hook B trigger metric**: "distinct miss events ≥3 over 10 sessions", not "miss_rate > 20%" (Attack 2)
3. **Scribe session-start catch-up routing pass**: Edit 1.5 in scribe-edit-plan.md (Attack 3)
4. **MCP embedder warm-up thread**: update to mcp-scaffold.md (Attack 4)
5. **DPO as v2 direction note**: add to parametric-spec.md (Attack 5)
6. **`has_table` threshold change**: 5 → 10 rows in linguist.md + scribe-edit-plan Edit 1.2 (Attack 7)

Attack 6 (continuous sweep) is filed as a retrospector lesson, not a deliverable change.

## Confidence after skeptic pass

**Medium-high**. Six corrections surfaced; all are additive refinements rather than direction changes. The deeper round's architecture is stable; the details are tightened.

## Handoff

- **adversary** — attack the SOURCES, not the synthesis
- **scribe-edit-plan** — apply the Edit 1.5 catch-up routing pass + the `has_table` threshold change
- **mcp-scaffold** — apply the embedder warm-up thread
- **parametric-spec** — add the DPO-as-v2 note
