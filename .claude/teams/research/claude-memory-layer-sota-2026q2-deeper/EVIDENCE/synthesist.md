# Synthesist — claim matrix and contradiction surfacing for deeper round

Sub-question: identify load-bearing contradictions across cartographer/librarian/historian/github-miner/tracer/linguist/empiricist/scribe-edit-plan/mcp-scaffold/hook-c-spike-plan/parametric-spec. Flag each for moderator debate if it affects the final answer.

## Method

- Read all 11 specialist-output evidence files written so far
- Build a claim matrix: one row per load-bearing claim, one column per cited specialist
- Identify contradictions (same-claim, different-verdict) AND identity-only differences (same verdict, different phrasing)

## Claim matrix (load-bearing claims only)

### Claim 1: Topic files live at the flat level, not in a subdirectory

| Specialist | Position | Evidence |
|-----------|----------|----------|
| cartographer | FLAT. `~/.claude/agent-memory/<agent>/<topic>.md`, NOT `<agent>/topic/<topic>.md` | Claude Code docs verbatim + existing Akash setup inspection |
| scribe-edit-plan | FLAT. Edit diffs use flat layout | Implements cartographer's position |
| tracer | FLAT. The lazy-load chain assumes flat discovery | Consistent with cartographer |
| github-miner | Notes ByteRover uses nested `<domain>/<topic>/<entry>.md` but Akash should NOT | Explicit disagreement with the brief's original phrasing |
| mcp-scaffold | (schema supports either but assumes flat) | Consistent with flat decision |

**Verdict**: **CONSENSUS (FLAT)**. The user's deeper-round brief said `~/.claude/agent-memory/<leader>/topic/<topic>.md`, which is a slip — correct path is `<leader>/<topic>.md`. Not a contradiction among specialists; a correction of the brief. Surface this to the user in SYNTHESIS.md.

### Claim 2: Python wins over Node for Hook B

| Specialist | Position | Evidence |
|-----------|----------|----------|
| empiricist | **PYTHON**, with quantitative table | Python has mature MCP SDK 1.27.0 + sqlite-vec 0.1.9 + sentence-transformers + stdlib FTS5 |
| librarian | Consistent — provides the exact Python package set | MCP Python SDK stable, sqlite-vec Python wheel |
| mcp-scaffold | Consistent — builds the Python scaffold | Uses empiricist's decision |
| github-miner | (notes ByteRover CLI is TypeScript but doesn't advocate TS for Akash's build) | Distinguishes ByteRover CLI adoption from Hook B design |

**Verdict**: **CONSENSUS (PYTHON)**. No contradiction.

### Claim 3: The pilot's 4-phase plan is not invalidated by the 14-day sweep

| Specialist | Position | Evidence |
|-----------|----------|----------|
| historian | Plan is validated + refined by ByteRover (2604.01599) AKL formula, maturity tiers, frontmatter schema | Verbatim AKL formulas from paper HTML |
| github-miner | Confirms ByteRover CLI exists, Elastic License 2.0, not a "just adopt this" alternative | Legal + architectural reasons |
| adversary-to-be | (not yet written, but inherits historian+github-miner verdicts) | - |

**Verdict**: **CONSENSUS (not invalidated, refined)**. No contradiction. But the refinements are substantive — the AKL formula is material.

### Claim 4: The scribe routing heuristic is `AND` (length AND type), not `OR`

| Specialist | Position | Evidence |
|-----------|----------|----------|
| linguist | `AND` — both length ≥1500 AND type condition must hold | Edge-case analysis with 8 examples |
| tracer | `AND` — matches the chain's failure modes (C1 over-route, C2 rule-loss) | Consistent |
| scribe-edit-plan | `AND` — implements linguist's predicate verbatim | Consistent |
| empiricist | (no specific position) | Not contested |

**Potential contradiction**: none of these actually DISAGREE, but the choice of `AND` vs `OR` is a decision point that deserves a moderator debate because changing it would change routing behavior dramatically.

**Verdict**: **CONSENSUS (AND)** but flag for a C-deeper-1 debate on whether `AND` is too conservative.

### Claim 5: Hook C one-evening spike is achievable and uses LatentMAS verbatim, not a from-scratch port

| Specialist | Position | Evidence |
|-----------|----------|----------|
| github-miner | LatentMAS repo is alive (last substantive code 2026-02-09), runnable, well-mapped | File tree + commit log verbatim |
| hook-c-spike-plan | Clone + install + smoke test + compare = 3-4 hours | Concrete step-by-step |
| empiricist | (not directly; defers to spike plan) | - |
| historian | LatentMAS fresh commits confirm repo is alive | Convergent |

**Verdict**: **CONSENSUS**. No contradiction.

### Claim 6: Parametric phase is a 6-month+ direction, NOT this quarter

| Specialist | Position | Evidence |
|-----------|----------|----------|
| empiricist | 4-6 years solo, 12-18 months with teams, to reach stability threshold | Lesson accumulation rate math |
| historian | LIMA + distil-labs support the dataset size; task family untested | Consistent with timeline |
| parametric-spec | Defers until stability gate is met; specifies the pipeline | Consistent |

**Verdict**: **CONSENSUS**. No contradiction.

### Claim 7: MemX ranker weights should be adjusted for Akash's workload

| Specialist | Position | Evidence |
|-----------|----------|----------|
| librarian | MemX defaults: 0.45/0.25/0.05/0.10 (sum 0.85) | Verbatim from paper § 3.4 |
| empiricist | Adjusted: 0.45/0.30/0.13/0.02 (sum 0.90) | Rationale: his corpus is small so frequency is useless; importance is high-signal |
| mcp-scaffold | Implements empiricist's adjusted weights | Consistent |

**Possible contradiction**: librarian reports the MemX values, empiricist ADJUSTS them. Is the adjustment justified?

- **Argument FOR adjustment**: Akash's corpus is small (~100-1000 lessons target in 12-18 months) while MemX's target corpus is 100K+ records. Frequency saturates at low counts; importance (scribe's "Reinforced by") is higher-signal than in a large corpus.
- **Argument AGAINST**: MemX's weights were empirically tuned on a benchmark; adjusting them without measurement is speculation. The MVP should use MemX defaults and adjust after observed recall failures.

**Verdict**: **CONDITIONAL CONTRADICTION** — flag for a moderator debate C-deeper-2: "Hook B MVP weights — MemX defaults or empiricist's adjustment?"

### Claim 8: ByteRover is NOT a replacement for Hook A, only a source of borrowed ideas

| Specialist | Position | Evidence |
|-----------|----------|----------|
| historian | Validation + source of AKL + schema + 5-tier retrieval — but NOT a drop-in replacement | Architecture + license analysis |
| github-miner | ByteRover CLI is Elastic 2.0 licensed, TypeScript, nested layout, too much delta to adopt | Legal + architectural |

**Implicit contradiction question**: is the skeptic going to argue "just adopt ByteRover"? This needs a pre-emptive skeptic attack.

**Verdict**: **PRE-EMPT (flag for skeptic attack 1)**. No specialist contradiction; just a known-incoming skeptic angle.

### Claim 9: The research-lead's Step 3 needs a "lazy pointer protocol" addition

| Specialist | Position | Evidence |
|-----------|----------|----------|
| cartographer | Required; docs don't cover this behavior | Docs analysis |
| tracer | Required; Chain B's failure mode C3 (orphan topic file) is mitigated by this | Chain analysis |
| linguist | Required; provides the exact phrasing | Vocabulary analysis |
| scribe-edit-plan | Implements it with an exact Edit diff | Consistent |

**Verdict**: **CONSENSUS**. No contradiction.

### Claim 10: The parametric phase timeline is years not months

| Specialist | Position | Evidence |
|-----------|----------|----------|
| empiricist | 4-6 years solo, 12-18 months with 5 teams | Accumulation rate math |
| historian | Supports: LIMA says 1000 examples works, Akash is far from that count | Consistent |
| parametric-spec | Explicitly gates on stability threshold not time | Consistent with empiricist |

**Verdict**: **CONSENSUS**. No contradiction.

## Summary of contradictions flagged for moderator

| ID | Contradiction | Moderator priority |
|----|--------------|--------------------|
| **C-deeper-1** | Scribe routing heuristic: `AND` (current linguist position) vs `OR` (not currently held by any specialist but worth checking) — is `AND` too conservative? | LOW (unanimous agreement; debate is prophylactic) |
| **C-deeper-2** | Hook B MVP weights: MemX defaults (0.45/0.25/0.05/0.10) vs empiricist's adjustment (0.45/0.30/0.13/0.02) | MEDIUM (real call with concrete defenders on both sides) |
| **SKEPTIC-1** | Pre-emptive: is ByteRover CLI a better "just adopt this" alternative to Hook A? | Handled by skeptic, not moderator |

## Other observations (not contradictions)

1. **The pilot's 4-phase plan survives this deeper round with two refinements**: (a) adopt ByteRover's AKL scoring formula verbatim in Hook A, (b) flag the user's `<leader>/topic/<topic>.md` path phrasing as a slip (correct is flat). Neither refinement invalidates the plan.

2. **Every specialist agrees on Python for Hook B and flat layout for Hook A**. The decisions are unambiguous.

3. **The 14-day sweep found 4 new arxiv papers** (ByteRover, Memory in LLM Era, MemMachine, PRIME) and **no invalidating commits** on the tracked competitor repos (Mem0, Letta, Graphiti, MemPalace, MemX, LatentMAS). The corpus is stable.

4. **MemMachine's LoCoMo 0.9169 claim** is another saturated-benchmark trap — pre-emptively rejected by the pilot's adversary ruling. No new action needed.

5. **LatentMAS's hybrid HF-vs-vLLM architecture** is a surprise finding. The compact-then-attend pattern uses HF Transformers for the latent step; vLLM is only used for text generation. This means the spike CANNOT just "use vLLM natively" — it has to keep HF around. Documented in hook-c-spike-plan.md.

## Handoff

- **moderator** — run C-deeper-1 and C-deeper-2 debates
- **skeptic** — pre-emptively attack the ByteRover adoption argument (SKEPTIC-1) AND the deeper round's own blind spots
- **adversary** — verify the 14-day sweep sources; check if any new source was pulled in without proper classification
- **evaluator** — 5-dim rubric against this round's SYNTHESIS.md (once written)

## Confidence

**High**. The claim matrix is comprehensive; every load-bearing claim is cited back to at least 2 specialists or a primary source. The two flagged contradictions are real and deserve moderator time.
