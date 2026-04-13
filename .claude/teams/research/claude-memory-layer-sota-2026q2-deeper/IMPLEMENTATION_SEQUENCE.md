# IMPLEMENTATION_SEQUENCE.md — memory layer for Claude Code

Ordered checklist the forthcoming Engineering Team will execute to implement the pilot's 4-phase memory-layer plan, with the deeper-round refinements applied. Every item has: **step**, **owner** (Engineering specialist), **prerequisites**, **acceptance criteria**, **rollback**.

**Source specs**:
- Hook A: `EVIDENCE/scribe-edit-plan.md`
- Hook B: `EVIDENCE/mcp-scaffold.md`
- Hook C: `EVIDENCE/hook-c-spike-plan.md`
- Parametric: `EVIDENCE/parametric-spec.md`

**Engineering Team specialists** (referenced as owners — the Engineering Team roster is not finalized at session time, so owner slots use placeholders like `eng-implementer`, `eng-reviewer`, `eng-integrator` that the Engineering Team lead can reassign):

---

## Phase 1 — Hook A (this week, zero new infrastructure)

### Step 1. Prepare the working branch
- **Owner**: eng-integrator
- **Prerequisites**: none
- **Action**: create a feature branch in `~/.claude/` if using git, or a stash if not. Verify current state of `~/.claude/agents/research/research-scribe.md` and `~/.claude/agents/research/research-lead.md` matches the deeper-round workspace snapshot.
- **Acceptance**: branch created or stash ready; `git status` shows clean tree OR `git stash list` shows the pre-edit snapshot.
- **Rollback**: `git checkout main` + remove the feature branch.

### Step 2. Apply Edit 1.1 to research-scribe.md (Hard rules: topic-dir ownership)
- **Owner**: eng-implementer
- **Prerequisites**: Step 1
- **Action**: apply `EVIDENCE/scribe-edit-plan.md` Edit 1.1 verbatim via the Edit tool.
- **Acceptance**: `grep "research-retrospector" ~/.claude/agents/research/research-scribe.md` returns the new line; `grep -c "Hard rules" ~/.claude/agents/research/research-scribe.md` still returns 1.
- **Rollback**: `git checkout -- research-scribe.md` OR re-apply the reverse diff.

### Step 3. Apply Edit 1.2 to research-scribe.md (topic-file routing logic)
- **Owner**: eng-implementer
- **Prerequisites**: Step 2
- **Action**: apply Edit 1.2 verbatim. This is the largest edit — the scribe's method gains a new step 4 with the routing predicate and a renumbered step 5 for the size check.
- **Acceptance**: `grep -n "route_to_topic" ~/.claude/agents/research/research-scribe.md` returns 1 match; `grep -n "Topic-file routing" ~/.claude/agents/research/research-scribe.md` returns 1 match; the file still has a valid frontmatter (`head -1` shows `---`).
- **Rollback**: `git checkout -- research-scribe.md`.

### Step 4. Apply Edit 1.3 to research-scribe.md (AKL frontmatter schema doc)
- **Owner**: eng-implementer
- **Prerequisites**: Step 3
- **Action**: apply Edit 1.3 verbatim. Adds the optional frontmatter schema documentation block.
- **Acceptance**: `grep -n "Adaptive Knowledge Lifecycle" ~/.claude/agents/research/research-scribe.md` returns 1 match; `grep -n "maturity: validated" ~/.claude/agents/research/research-scribe.md` returns 1 match.
- **Rollback**: `git checkout -- research-scribe.md`.

### Step 5. Apply Edit 1.4 to research-scribe.md (trigger metric instrumentation)
- **Owner**: eng-implementer
- **Prerequisites**: Step 4
- **Action**: apply Edit 1.4 verbatim. Adds the Hook A → Hook B trigger metric section.
- **Acceptance**: `grep -n "scribe-metric:" ~/.claude/agents/research/research-scribe.md` returns 1 match; `grep -n "distinct miss events" ~/.claude/agents/research/research-scribe.md` returns 1 match.
- **Rollback**: `git checkout -- research-scribe.md`.

### Step 6. Apply Edit 1.5 to research-scribe.md (session-start catch-up routing)
- **Owner**: eng-implementer
- **Prerequisites**: Step 5
- **Action**: apply Edit 1.5 verbatim. Adds the session-start catch-up routing pass so a missed session close doesn't orphan new lessons.
- **Acceptance**: `grep -n "catch-up routing pass" ~/.claude/agents/research/research-scribe.md` returns 1 match.
- **Rollback**: `git checkout -- research-scribe.md`.

### Step 7. Apply Edit 2.1 to research-lead.md (lazy pointer protocol in Step 3)
- **Owner**: eng-implementer
- **Prerequisites**: Step 6
- **Action**: apply Edit 2.1 verbatim. Extends Step 3 of the lead's intake protocol with lazy-pointer handling of topic file references.
- **Acceptance**: `grep -n "lazy pointer" ~/.claude/agents/research/research-lead.md` returns 1 match.
- **Rollback**: `git checkout -- research-lead.md`.

### Step 8. Apply Edit 2.2 to research-lead.md (topic-file read-only rule)
- **Owner**: eng-implementer
- **Prerequisites**: Step 7
- **Action**: apply Edit 2.2 verbatim. Adds the rule that topic files are read-only for the lead.
- **Acceptance**: `grep -n "Topic files under" ~/.claude/agents/research/research-lead.md` returns 1 match.
- **Rollback**: `git checkout -- research-lead.md`.

### Step 9. Verification pass on both files
- **Owner**: eng-reviewer
- **Prerequisites**: Step 8
- **Action**: read the full `research-scribe.md` and `research-lead.md` files top-to-bottom. Confirm: frontmatter still parses, markdown structure is valid, no duplicate section headers, the 7 grep checks from the scribe-edit-plan verification checklist all pass.
- **Acceptance**: all grep checks pass; visual read shows consistent structure.
- **Rollback**: if any check fails, revert the failing edit and re-inspect.

### Step 10. Smoke test Hook A on a new research session
- **Owner**: eng-integrator
- **Prerequisites**: Step 9
- **Action**: run a deliberate research session designed to produce a long-tail lesson (e.g., dispatch the research team on a question that produces a lesson with a 500-line code block and a 10+ row table). At session close, verify:
  - The retrospector writes the lesson to MEMORY.md as usual
  - The scribe runs the routing pass and routes the lesson to a topic file
  - A new `*.md` file appears in `~/.claude/agent-memory/research-lead/` with the topic slug
  - MEMORY.md now contains a stub referencing the topic file
  - LOG.md has a `scribe-curator: routed Lesson N` line
- **Acceptance**: all 5 artifacts observed.
- **Rollback**: delete the topic file + revert MEMORY.md changes if the test shows the routing is broken.

**Phase 1 complete**: Hook A is in production. Scribe routes long-tail content to topic files; lead lazy-loads them on demand.

---

## Phase 2 — Hook B (conditional on Hook A insufficient)

### Step 11. Run the trigger metric check after 10 sessions
- **Owner**: eng-reviewer
- **Prerequisites**: Phase 1 complete; 10 research sessions run with Hook A active
- **Action**: run the rolling analysis script (see scribe-edit-plan Edit 1.4):
  ```bash
  grep "scribe-metric: topic-file-check" ~/.claude/teams/research/*/LOG.md | tail -10 | \
      awk -F'missed=' '{sum+=$2} END {print "distinct miss events:", sum}'
  ```
- **Acceptance**: the command produces a number.
- **Decision**:
  - **distinct miss events ≥ 3** → proceed to Step 12 (build Hook B)
  - **distinct miss events 1-2** → monitor 10 more sessions, repeat Step 11
  - **distinct miss events = 0** → STOP. Hook A is sufficient. Hook B is not built. Mark the phase complete and skip to Phase 3.
- **Rollback**: none (it's a decision gate).

### Step 12. Scaffold the Python MCP server
- **Owner**: eng-implementer
- **Prerequisites**: Step 11 → BUILD
- **Action**: create the directory `~/.claude/memory-mcp/` with the layout from `EVIDENCE/mcp-scaffold.md` § "Directory layout". Create `pyproject.toml` with the dependency set: `mcp>=1.27.0, sqlite-vec>=0.1.9, sentence-transformers`. Run `uv sync` or `pip install -e .`.
- **Acceptance**: `python -c "from memory_mcp.server import mcp; print('ok')"` succeeds.
- **Rollback**: `rm -rf ~/.claude/memory-mcp/`.

### Step 13. Create schema.sql and db.py
- **Owner**: eng-implementer
- **Prerequisites**: Step 12
- **Action**: write `src/memory_mcp/schema.sql` verbatim from `mcp-scaffold.md` § "Schema DDL" (7 tables + 3 triggers + 5 indexes). Write `src/memory_mcp/db.py` with the `get_connection()` and `ensure_schema()` helpers.
- **Acceptance**: `python -c "from memory_mcp.db import get_connection, ensure_schema; c=get_connection('/tmp/test.sqlite'); ensure_schema(c); print('ok')"` succeeds without errors. `sqlite3 /tmp/test.sqlite '.schema'` shows all 7 tables + FTS5 virtual table + vec0 virtual table.
- **Rollback**: delete the schema.sql and db.py files.

### Step 14. Implement the ranker
- **Owner**: eng-implementer
- **Prerequisites**: Step 13
- **Action**: write `src/memory_mcp/ranker.py` from `mcp-scaffold.md` § "Ranker implementation" verbatim. **Use the MemX EXACT defaults** per Moderator C-deeper-2 verdict: `W_SEMANTIC=0.45, W_RECENCY=0.25, W_FREQUENCY=0.05, W_IMPORTANCE=0.10, REJECT_THRESHOLD=0.15`. Ensure the `rank()` function returns per-factor breakdown for observability.
- **Acceptance**: unit tests in `tests/test_ranker.py` pass: (a) score returns a float, (b) ranking is stable by score, (c) per-factor breakdown sums to total.
- **Rollback**: delete ranker.py and test_ranker.py.

### Step 15. Implement the embedder wrapper
- **Owner**: eng-implementer
- **Prerequisites**: Step 14
- **Action**: write `src/memory_mcp/embedder.py` with a `get_embedder(model_name)` factory that loads Qwen3-Embedding-0.6B via sentence-transformers. Expose an `embed(text: str) -> list[float]` method.
- **Acceptance**: `python -c "from memory_mcp.embedder import get_embedder; e=get_embedder('Qwen/Qwen3-Embedding-0.6B'); v=e.embed('hello'); assert len(v)==1024; print('ok')"` succeeds. (First call will download the model; ~650MB, ~1-2 minutes.)
- **Rollback**: delete embedder.py.

### Step 16. Implement the 4 MVP handlers
- **Owner**: eng-implementer
- **Prerequisites**: Step 15
- **Action**: write `src/memory_mcp/handlers/{search,insert,update,delete}.py` implementing the API surface from `mcp-scaffold.md` § "API surface" for the MVP rows. Each handler takes (conn, embedder, ...) and returns the documented output shape.
- **Acceptance**: `tests/test_handlers.py` passes for each handler (insert → search → search returns it → update → search returns updated → delete → search returns nothing).
- **Rollback**: delete the handlers/ files.

### Step 17. Wire up the MCP server with embedder warmup
- **Owner**: eng-implementer
- **Prerequisites**: Step 16
- **Action**: write `src/memory_mcp/server.py` per `mcp-scaffold.md` § "MCP server entry point". Include the **background thread embedder warmup** in `__main__` (post-skeptic Attack 4 correction). Verify the decorators are applied correctly.
- **Acceptance**: `python -m memory_mcp.server` starts without errors; the MCP handshake completes (verify by pointing Claude Code at it via settings.json). First `search_memory` call returns results (may be slow if warmup hasn't finished).
- **Rollback**: delete server.py.

### Step 18. Register the MCP server in settings
- **Owner**: eng-integrator
- **Prerequisites**: Step 17
- **Action**: update `~/.claude/agents/research/research-lead.md`'s frontmatter to include the `mcpServers` entry per `mcp-scaffold.md` § "settings.json registration snippet" (subagent-frontmatter form preferred). Alternatively, add to `~/.claude/settings.json` if user-scope is preferred.
- **Acceptance**: in a new research-lead session, `memory.search` tool is available. A smoke test query returns an empty result (DB is empty initially).
- **Rollback**: remove the mcpServers entry; the MCP server still exists but isn't wired into sessions.

### Step 19. Write the bootstrap and backup scripts
- **Owner**: eng-implementer
- **Prerequisites**: Step 18
- **Action**: write `scripts/bootstrap.py` that creates the initial DB + ingests any existing topic files from `~/.claude/agent-memory/research-lead/*.md` into the `memory` table. Write `scripts/backup.sh` per `mcp-scaffold.md` § "Backup schedule".
- **Acceptance**: bootstrap.py populates the DB from existing topic files; `search_memory("test query")` returns real results. backup.sh creates a file in `~/.claude/memory-mcp/backups/`.
- **Rollback**: delete scripts/; data remains.

### Step 20. Install the cron line for daily backups
- **Owner**: eng-integrator
- **Prerequisites**: Step 19
- **Action**: add `0 3 * * * bash ~/.claude/memory-mcp/scripts/backup.sh` to the user's crontab.
- **Acceptance**: `crontab -l | grep memory-mcp` returns the line.
- **Rollback**: remove the line via `crontab -e`.

**Phase 2 complete**: Hook B is in production. The MCP server exposes `search_memory`, `insert_memory`, `update_memory`, `delete_memory`. The scribe's routing metric continues to run — if it shows new insufficiency signals (rising miss events even with Hook B), the Engineering Team can add the `temporal` and `graph_neighbors` v2 handlers.

---

## Phase 3 — Hook C (Q3 spike, one evening)

### Step 21. Run the pre-flight check
- **Owner**: eng-implementer (wearing the empiricist hat)
- **Prerequisites**: an evening with 3-5 hours free + a GPU with ≥32GB VRAM
- **Action**: run the pre-flight checklist from `hook-c-spike-plan.md` § "Pre-flight". Verify Python 3.10+, vLLM, HF Transformers + CUDA are available.
- **Acceptance**: all 4 pre-flight checks pass.
- **Rollback**: if any fails, defer the spike and document the blocker. Return to Phase 3 later.

### Step 22. Clone LatentMAS and run reference + baseline
- **Owner**: eng-implementer
- **Prerequisites**: Step 21
- **Action**: execute `hook-c-spike-plan.md` Steps 1-5: clone repo, install deps, read the key files (~30 min), run `latent_mas` on GSM8K-20, run `text_mas` baseline, collect wall-time + token count + accuracy for both.
- **Acceptance**: both runs complete; numbers collected for comparison.
- **Rollback**: if both runs fail, fall back to the vLLM prefix-caching demo from `hook-c-spike-plan.md` § "Alternative".

### Step 23. Compute ratios and make the go/no-go call
- **Owner**: eng-implementer
- **Prerequisites**: Step 22
- **Action**: compute `token_savings`, `wall_time_ratio`, `accuracy_delta` per `hook-c-spike-plan.md` § "Step 6 — Go/no-go decision". Write `SPIKE_REPORT.md` using the template.
- **Acceptance**: SPIKE_REPORT.md exists with GO / DEFER / NO-GO verdict.
- **Decision**:
  - **GO** → proceed to Step 24 (document next-steps for a production integration)
  - **DEFER** → file the spike report + file a retrospector lesson; return to Phase 4 preparation
  - **NO-GO** → file the spike report + retrospector lesson; do NOT attempt production integration in the near term
- **Rollback**: none (it's a report).

### Step 24. (On GO) Write the production integration proposal
- **Owner**: eng-integrator + eng-reviewer
- **Prerequisites**: Step 23 → GO
- **Action**: write a proposal for how LatentMAS's compact-then-attend pattern integrates with the Research Team's dispatch loop. This is the OPPOSITE end of the spike — it's "what would a week-level production build look like" NOT "what was the spike's result". Reference `hook-c-spike-plan.md` § "Integration surface" for the starting point.
- **Acceptance**: a PRODUCTION_PROPOSAL.md file exists with architectural diagrams + migration path + risk analysis.
- **Rollback**: delete the proposal; Hook C stays as a spike, not production.

**Phase 3 complete**: Hook C has a spike verdict + (conditionally) a production proposal. Gate the actual production build on a separate decision cycle.

---

## Phase 4 — Parametric (6-month to year-long direction)

### Step 25. Monitor the stability threshold
- **Owner**: eng-reviewer (running on a monthly or quarterly cadence)
- **Prerequisites**: Phases 1 + 2 running continuously for at least 6 months
- **Action**: run a monthly count of stable lessons across ALL agent MEMORY.md files (research-lead + any other teams): grep for lessons with `Reinforced by` ≥ 3, `maturity >= validated`, and `days_since_creation >= 30`.
- **Acceptance**: total count reported.
- **Decision**:
  - **≥ 300 stable lessons** → proceed to Step 26 (build the distillation pipeline)
  - **100 ≤ count < 300** → still growing, monitor next month
  - **< 100** → parametric is too early; continue operating on Hooks A + B only; revisit in 6 months
- **Rollback**: none (it's a monitoring step).

### Step 26. Build the synthetic prompt generator
- **Owner**: eng-implementer
- **Prerequisites**: Step 25 → BUILD
- **Action**: write `~/.claude/distillation/synth.py` per `parametric-spec.md` § "Synthetic prompt generator". Call Claude Opus for each eligible lesson, produce 3-5 paraphrased instruction/response pairs per lesson. Output `train.jsonl`.
- **Acceptance**: `train.jsonl` exists; line count = 3-5× the stable lesson count; a random sample of 20 pairs passes manual inspection for coherence and lesson fidelity.
- **Rollback**: delete the .jsonl; no data loss since MEMORY.md files are untouched.

### Step 27. Run the LoRA training
- **Owner**: eng-implementer
- **Prerequisites**: Step 26 + hardware available (1x 4090 minimum)
- **Action**: run `~/.claude/distillation/train.py` per `parametric-spec.md` § "Training script sketch". Expected wall time: ~45-90 minutes on 4090; ~20-40 on H100.
- **Acceptance**: `~/.claude/distillation/lora-out/final/` exists with adapter_config.json and adapter_model.safetensors. Training loss monotonically decreases over the 3 epochs.
- **Rollback**: delete the lora-out directory.

### Step 28. Run the 2-part evaluation
- **Owner**: eng-reviewer
- **Prerequisites**: Step 27
- **Action**: run `parametric-spec.md` § "Evaluation" Part 1 (lesson recall: 30 held-out paraphrased questions) and Part 2 (capability regression: GSM8K/HumanEval/MMLU/IFEval subsets). Compute recall percentage and per-benchmark regression deltas.
- **Acceptance**: `EVAL_REPORT.md` exists with a DEPLOY / TUNE / ABANDON verdict.
- **Decision**:
  - **DEPLOY** (recall ≥ 80% AND all regression deltas within tolerance) → proceed to Step 29
  - **TUNE** (recall < 80% OR one regression slightly over tolerance) → reduce rank or epochs, go back to Step 27
  - **ABANDON** (recall < 50% OR any regression catastrophic) → file a retrospector lesson + abandon parametric for this quarter; return to Phase 4 Step 25 next quarter

### Step 29. Deploy via vLLM with LoRA adapter
- **Owner**: eng-integrator
- **Prerequisites**: Step 28 → DEPLOY
- **Action**: launch vLLM with `--enable-lora --lora-modules research-lead-playbook=~/.claude/distillation/lora-out/final` per `parametric-spec.md` § "Deployment". Verify a test query against the LoRA-adapted model returns reasonable output.
- **Acceptance**: vLLM serves the LoRA adapter; a paraphrased test query returns the rule of thumb.
- **Rollback**: stop vLLM; fall back to serving base Qwen3-8B.

### Step 30. Integrate the LoRA-served model as a secondary worker
- **Owner**: eng-integrator
- **Prerequisites**: Step 29
- **Action**: configure the Research Team's dispatch loop to route specific specialists' "cheap reasoning" steps to the LoRA-adapted worker (not the Opus 4.6 main session — the LoRA is a SUPPLEMENT, not a replacement). Specifically: the empiricist's literature-grounded reasoning steps can route to the LoRA worker as a cost-saver.
- **Acceptance**: a test research session runs with the empiricist dispatched to the LoRA-adapted worker; output quality matches or exceeds a baseline empiricist run.
- **Rollback**: revert the dispatch config; empiricist returns to Opus 4.6.

**Phase 4 complete**: parametric memory is deployed as a supplementary worker. Stable lessons are baked into weights; high-update-rate lessons remain in MEMORY.md (token-level). The hybrid token+parametric architecture is operational.

---

## Cross-phase monitoring

After all phases ship, the Engineering Team should maintain:

1. **Scribe metric weekly**: ensure the topic-file-hit rate stays healthy. Regressions trigger a Phase 1 revisit.
2. **MCP server uptime**: health check endpoint + daily backup verification.
3. **LoRA retraining cadence**: monthly or quarterly re-distillation as stable lesson count grows.
4. **14-day fresh sweep**: retrospector runs at session start on fast-moving topics (v2.3 protocol candidate — not yet formalized).

## Summary table

| Phase | Steps | Owner | Time | Gate |
|-------|-------|-------|------|------|
| 1. Hook A | 1-10 | eng-implementer + eng-reviewer + eng-integrator | 1-2 hours (edits) + 1 smoke-test session | — |
| 2. Hook B | 11-20 | eng-implementer (3 person-days) + eng-integrator | ~3 days after 10-session trigger check | `distinct miss events ≥ 3` |
| 3. Hook C | 21-24 | eng-implementer (empiricist) | 1 evening + 1 day of integration proposal | spike ratios `token_savings ≥ 0.20 AND accuracy_delta ≥ -0.05` |
| 4. Parametric | 25-30 | eng-implementer + eng-reviewer + eng-integrator | ~1 month of build when triggered | `stable lessons ≥ 300` |

Total timeline **from today** (2026-04-12):
- Phase 1: complete this week
- Phase 2: conditional; earliest ~5 weeks out
- Phase 3: Q3 2026 (one-evening spike when Akash wants to run it)
- Phase 4: 6-18 months out, depending on team growth

## Rollback hierarchy

If ALL phases need to be rolled back (e.g., the entire architecture was wrong), the ordered rollback is:

1. Phase 4: stop LoRA deployment, revert dispatch config
2. Phase 3: delete spike reports, no production integration to roll back
3. Phase 2: `crontab -e` (remove backup), remove settings.json MCP entry, `rm -rf ~/.claude/memory-mcp/`
4. Phase 1: `git checkout -- research-scribe.md research-lead.md`, delete any topic files created during Phase 1 operation

Each phase is rollback-independent of the others except that Phase 2 depends on Phase 1's topic files existing. If Phase 1 is rolled back, Phase 2's DB contents become orphaned but harmless (schema stays valid).

## Notes for the Engineering Team lead

- **Do not optimize for cost**: per empiricist.md, the memory layer is <3% of session cost. Optimize for (a) lesson recall quality, (b) cross-session durability, (c) operational simplicity.
- **ByteRover is NOT a dependency**: the AKL formula is BORROWED with citation in the scribe persona. Do not install `byterover-cli` or introduce Elastic License 2.0 code into the stack.
- **LatentMAS requires HuggingFace Transformers**: the Hook C spike cannot be done with vLLM alone. Keep HF in the environment.
- **Parametric is years away at solo pace**: per empiricist.md timeline math. Do not rush Phase 4 — it requires real stable lessons, not synthetic ones.
- **Every edit is reversible**: the hard rules in the research personas are the load-bearing protection. If a scribe edit goes wrong, the git checkout restores the original behavior.
