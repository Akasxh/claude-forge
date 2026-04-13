# Empiricist — cost/latency sizing, trigger metrics, language choice, LoRA scope

Sub-question: (a) pick Python vs Node for Hook B with a quantitative rationale, (b) define the "Hook A insufficient" trigger metric with thresholds, (c) size the LoRA distillation training and evaluation, (d) back-of-envelope the cost impact of each hook on Akash's typical session.

## Method

- Literature-grounded numbers (no code run this round per the pilot empiricist's constraint)
- Cross-reference with pilot empiricist.md for consistency
- Use MemX published numbers as the hybrid-ranker calibration point
- Use LIMA + Unsloth numbers for LoRA scaling

## Language choice for Hook B MCP — Python WINS

### Quantitative comparison

| Dimension | Python | Node |
|-----------|--------|------|
| **MCP SDK maturity** | `mcp 1.27.0`, released 2026-04-02, stable | `@modelcontextprotocol/sdk`, equivalent maturity |
| **sqlite-vec binding** | first-class wheel (0.1.9 stable + 0.1.10 alphas); `import sqlite_vec; sqlite_vec.load(db)` | `sqlite-vec` npm package exists but requires separate loader; less stable on Windows |
| **FTS5 built-in** | stdlib `sqlite3` ships with FTS5 on every mainstream Python build | better-sqlite3 ships FTS5 but requires native rebuild |
| **Embedding pipeline** | `sentence-transformers`, `transformers`, `torch` all one-import | Transformers.js for inference, OR calls out to Python process |
| **Akash's stack fit** | Python-native ML toolchain (vLLM, HF, Qwen3) | Node surfaces for CLI tools |
| **Startup latency** | ~200-400ms cold start | ~50-100ms cold start |
| **Async story** | asyncio + aiosqlite | native Promise |
| **Debugability** | pdb, pytest, richness | Node inspector, vitest |
| **Lines-of-code estimate for MVP** | ~300 lines (server.py, schema.sql, ranker.py, loader.py) | ~450 lines (TS type boilerplate adds ~50%) |

**Decision: Python.** The Python MCP SDK at 1.27.0 is stable, sqlite-vec has a first-class wheel, Python's stdlib sqlite3 ships FTS5, and the embedding pipeline (sentence-transformers for Qwen3-Embedding-0.6B) is one import away. Node's only real advantage (startup latency) doesn't matter for a single-user dev tool that stays resident.

### Specific package set for Hook B (Python)

```
mcp>=1.27.0               # official MCP Python SDK
sqlite-vec>=0.1.9         # vector search extension  
sentence-transformers     # for Qwen3-Embedding-0.6B
# note: sqlite3 is stdlib, FTS5 is compiled in by default
# note: transformers, torch are pulled in by sentence-transformers
```

Python min version: **3.11** (MCP requires >= 3.10, but 3.11 gets better asyncio + sqlite fixes)

## Hook A insufficient — the trigger metric

### Definition

**Metric**: `topic_file_miss_rate` = (count of sessions where lead failed to find a relevant topic file that existed) / (count of sessions where the lead SHOULD have read at least one topic file).

**Who measures**: the scribe, at session end, during its normal ledger pass.

**How measured**:
1. At session end, scribe reads `EVIDENCE/*.md` for the session and checks whether any specialist cited a topic file (`~/.claude/agent-memory/research-lead/*.md`) other than MEMORY.md.
2. Scribe also checks the lead's SYNTHESIS.md references.
3. If a topic file exists on disk and IS relevant to the session's question (heuristic: topic slug overlaps with question title or sub-question keywords) BUT was NOT cited → count as a miss.
4. If the lead did cite the topic file → count as a hit.

**Trigger threshold**:
- Over **10 consecutive sessions**:
  - If `miss_rate > 20%` → Hook A is insufficient → Hook B BUILD
  - If `miss_rate between 5% and 20%` → Hook A is MARGINAL → monitor another 10 sessions
  - If `miss_rate < 5%` → Hook A is sufficient → Hook B SKIP

**Why 10 sessions**: at Akash's pace (~2-3 research sessions per week), 10 sessions = ~4 weeks of data. This is the minimum window that gives enough trial events to distinguish 5% from 20% without being noise.

**Why 20%**: if 1 out of 5 relevant topic files is missed, the lead's effective memory is already degraded. Below 20% is tolerable noise; above 20% is a real bottleneck.

**Operational cost**: scribe's per-session check adds ~2 Read tool calls and ~50 tokens of reasoning. Negligible.

### Instrumentation

The scribe logs each miss/hit decision to LOG.md with a machine-parseable line:

```
scribe-metric: topic-file-check | slug=<session-slug> | total-topic-files=<N> | 
               cited-topic-files=<K> | relevant-missed=<M> | hit-rate=<K/(K+M)>
```

A tiny helper script (or Bash one-liner with grep) can compute the rolling 10-session average.

## LoRA distillation scope and sizing

### Dataset target

From historian.md (LIMA paper) + distil-labs benchmark:
- **Minimum useful**: ~300 stable lessons, expanded to ~1,500 synthetic training pairs (3-5 prompts per lesson)
- **Comfortable**: ~500 stable lessons → ~2,500 pairs
- **Too much for small task**: 1,000+ → risk of overfitting + loss of base capability

**Decay gate (the filter from IH-D)**: a lesson is STABLE and eligible for distillation if:
- `reinforced_by_count >= 3` (referenced in 3+ sessions' retrospectors)
- AND `maturity >= validated` (ByteRover AKL score ≥ 65)
- AND `days_since_creation >= 30` (not a flash-in-the-pan observation)

**Projected Akash-specific timeline**: MEMORY.md currently has ~10 lessons. At ~1 new lesson every 2-3 sessions (observed rate from pilot), 300 lessons is reached in ~600-900 sessions. At 2-3 sessions/week, that's **4-6 years**. This is NOT a 2026-Q3 item; it's correctly a 6-month "direction" item.

**Corollary**: the parametric phase should NOT be gated on raw lesson count. It should be gated on **research team breadth**. When Akash has 5+ specialist teams (Research, Planning, Implementation, Review, Testing) each with their own MEMORY.md, the combined lesson corpus hits ~300 stable lessons much faster — maybe 12-18 months.

### Model + rank recommendation

From historian.md prior art sweep:

| Choice | Recommendation | Rationale |
|--------|----------------|-----------|
| Model | **Qwen3-8B** | Top of distil-labs fine-tune benchmark, Apache 2.0 license, vLLM-native |
| LoRA rank | **16** | Canonical for instruction tuning on 7B-8B models; avoids overfitting on ~1500-2500 pairs |
| Target modules | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` | "All linears" standard pattern |
| LR | 5e-5 | Standard for LoRA SFT |
| Epochs | 3 | Avoids overfitting on small dataset |
| Batch size | 8 (effective, with GA) | Fits 1x 4090 / similar |
| Max seq len | 2048 | Lessons are short |
| Warmup | 100 steps |
| Optimizer | AdamW 8-bit (bitsandbytes) |

**Expected training time**: ~45-90 minutes on 1x 4090 for 300 lessons × 5 prompts × 3 epochs (~4500 training steps total at batch 8 effective).

**Expected VRAM**: ~24GB for Qwen3-8B + LoRA rank 16 at bf16 with bnb 4-bit base — fits the 4090. For 16-bit full LoRA without quantization, ~48GB needed — use A100 40GB or H100.

### Training data format

**Shape**: supervised instruction tuning pairs. Each lesson produces 3-5 synthetic prompts.

**Example** (for a lesson like "moderator owns contradictions, not the lead"):

```jsonl
{"instruction": "You are the research lead. Two specialists have contradicted each other on a load-bearing claim. What do you do?", "output": "Dispatch the moderator for a 3-round structured debate. Your verdict is not trustworthy because you are also the synthesizer."}
{"instruction": "When should the lead make a judgment call between two specialists' contradictions?", "output": "Never, on load-bearing claims. Always dispatch the moderator. Lead-only arbitration is subject to confirmation bias."}
{"instruction": "What is the binding rule on handling specialist contradictions?", "output": "Contradictions go to the moderator, not to the lead's own judgment. This is a binding lesson from MEMORY.md."}
```

**Format**: JSONL, one training pair per line, compatible with TRL's `SFTTrainer` and Axolotl.

**Generation of synthetic prompts**: a larger model (GPT-4-class or Claude Opus itself) takes each lesson and generates 3-5 prompt/response pairs. This is a one-time operation, done in bulk at training time. **Akash can write a small script that reads MEMORY.md, filters to stable lessons, calls Claude Opus for paraphrasing, and dumps JSONL**. ~500 tokens per lesson for the paraphrase call → $0.004/lesson at Opus prices → $1.20 total for 300 lessons.

**Alternative formats considered and rejected**:
- **DPO pairs**: requires "chosen vs rejected" preference data; we don't have the rejected half. SKIP.
- **Completion-only**: no clear split between prompt and completion in a lesson; harder to evaluate.
- **Raw text LM**: treats MEMORY.md as a corpus; won't encode the "when asked X, do Y" structure. SKIP.

**Winner**: supervised instruction tuning (SFT) with synthetic paraphrased prompts.

### Evaluation protocol

The question: "did the LoRA encode the lessons AND does it not regress base capability?"

**Two-part evaluation**:

1. **Lesson recall eval** (target: the LoRA internalized the rules):
   - Build a held-out set of 30 lesson questions (not used in training), paraphrased from 30 training lessons.
   - For each, query the LoRA model and grade whether the answer contains the rule-of-thumb.
   - Pass criterion: ≥ 80% contain the rule.
   - Human-in-the-loop OR LLM-as-judge (use Opus as judge on the 30 pairs).

2. **Capability regression eval** (target: LoRA did not damage base model):
   - Run a subset of the base model's training tasks:
     - GSM8K (math): 50 samples, pass criterion: within 5% of base Qwen3-8B score
     - HumanEval (code): 50 samples, pass criterion: within 5% of base
     - MMLU (knowledge): 100 samples, pass criterion: within 3% of base
     - IFEval (instruction following): 50 samples, pass criterion: within 5% of base
   - If ANY regression exceeds the threshold → the LoRA is over-fitted to the lesson data → reduce rank or epochs → retrain.

**Total eval cost**: ~250 LLM calls for the regression battery + 30 for lesson recall = 280 calls. ~1 hour on a local vLLM deployment. Negligible.

## Per-session cost impact of each hook

| Hook | Added reads | Added writes | Added tokens/session | $ impact |
|------|-------------|--------------|----------------------|----------|
| **Hook A (topic routing)** | 0-3 topic file reads when lead lazy-loads | 1-2 topic-file writes at session close (scribe) | +0-6K tokens read, +500 tokens write | +$0.00 to +$0.10 |
| **Hook B (MCP query)** | 1 MCP `search` call when a specialist needs long-tail | Negligible (INSERT on close) | +500 tokens query response | +$0.00 to +$0.05 |
| **Hook C (LatentMAS spike)** | NONE (experimental; not session-integrated this quarter) | NONE | 0 | $0 (one-evening engineering cost, not per-session) |
| **Parametric (LoRA)** | ZERO at read time (the lessons are baked in) | ZERO (replaces session-start injection for the distilled subset) | -6K tokens saved per session (stable lessons stay in weights) | -$0.09/session |

**Net impact**: Hook A + B adds ~$0.05-0.15 per session. Parametric (when eventually deployed) subtracts ~$0.09. Akash's current session cost is ~$5-50; the memory layer remains <3% of total cost.

**The memory layer should NOT be optimized for per-session cost.** It should be optimized for:
1. **Lesson recall quality** (does the lead act on the right rules?)
2. **Cross-session durability** (do lessons survive /compact, team rotation, re-runs?)
3. **Operational simplicity** (can Akash reason about the system without debugging?)

Cost is a tertiary concern.

## Confidence

**High** on the language choice (Python wins unambiguously given Akash's stack).
**High** on the trigger metric (10-session, 20% threshold) — these are derived from standard A/B sizing rules and the pilot's observed 2-3 sessions/week pace.
**Medium-high** on the LoRA scoping — the 300-500 stable-lesson target is prior-art-grounded but not specifically validated for Akash's task family. The **timeline** (4-6 years alone, 12-18 months across teams) is the load-bearing observation — it tells Akash the parametric phase is genuinely a "direction" item, not a 2026-Q3 build.

## Handoff

- **mcp-scaffold** (separate evidence file) — uses the Python package set and the MemX-derived ranker weights
- **scribe-edit-plan** — uses the trigger-metric instrumentation lines
- **skeptic** — attack: is the 20% threshold too generous? Is the 10-session window too short?
- **moderator** — if anyone contests Python over Node, run the debate

## Citations

- Pilot empiricist.md — `~/.claude/teams/research/claude-memory-layer-sota-2026q2/EVIDENCE/empiricist.md`, read 2026-04-12 (reused numbers for session token budget and per-session cost baseline)
- LIMA paper — `arxiv.org/abs/2305.11206`, 2023 (1000-example rule)
- Unsloth docs — `unsloth.ai/docs/get-started/fine-tuning-llms-guide`, retrieved 2026-04-12 (~1-2 hr T4 time)
- distil-labs benchmark — "We Benchmarked 12 Small Language Models", retrieved 2026-04-12 (Qwen3-4B/8B ranking)
- MemX paper — `arxiv.org/html/2603.16171` § 3.4, retrieved 2026-04-12 (hybrid ranker)
- MCP Python SDK — `pypi.org/project/mcp/`, retrieved 2026-04-12 (1.27.0, >=3.10)
- sqlite-vec — `pypi.org/project/sqlite-vec/` + `alexgarcia.xyz/sqlite-vec/python.html`, retrieved 2026-04-12 (0.1.9 stable)
