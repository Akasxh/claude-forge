# Hook C — LatentMAS spike plan for a single evening

This is the one-evening Hook C prototype scope. Akash can execute it in 3-5 hours of focused time on his existing vLLM + Qwen3-14B setup. The plan is a literal checklist — every item has a concrete action and a measurable success criterion.

## Pre-flight (0:00 — 0:15, before the clock starts)

Verify the environment is ready:

```bash
# 1. Python env available
python --version  # expect 3.10+

# 2. vLLM installed and Qwen3-14B pullable
python -c "from vllm import LLM; print('vllm ok')"

# 3. HuggingFace transformers + torch available (LatentMAS needs both)
python -c "from transformers import AutoModelForCausalLM; import torch; print(torch.cuda.is_available())"

# 4. At least one GPU with >= 32GB VRAM (14B in bf16 + KV cache workspace)
nvidia-smi
```

If any check fails, the spike is blocked and the outcome is "document the blocker; defer." This is an allowed termination.

## Step 1 — Clone and inspect (0:15 — 0:30)

```bash
cd ~/PROJECTS  # or wherever Akash keeps experiments
git clone https://github.com/Gen-Verse/LatentMAS.git
cd LatentMAS
git log --oneline -10  # expect b9b2095 (2026-03-27) at top
ls methods/            # expect baseline.py, text_mas.py, latent_mas.py
wc -l methods/latent_mas.py  # expect ~420 lines
wc -l models.py                # expect ~340 lines
```

**Success criterion**: repo cloned, `methods/latent_mas.py` and `models.py` are present and non-trivial.

## Step 2 — Install dependencies (0:30 — 0:45)

```bash
cd ~/PROJECTS/LatentMAS

# Create isolated env
conda create -n latentmas python=3.10 -y
conda activate latentmas

# LatentMAS's own requirements (per README)
pip install -r requirements.txt
# Resolves to: transformers, torch, numpy, tqdm, accelerate, datasets

# vLLM (optional per LatentMAS but required for Akash's intended deployment)
pip install vllm

# Check
python -c "from methods.latent_mas import LatentMASMethod; print('latent_mas importable')"
python -c "from vllm import LLM; print('vllm importable')"
```

**Success criterion**: both imports succeed without errors. If an import fails, inspect `pip install` output and fix. Typical issues: torch/vllm version mismatch.

## Step 3 — Read the key files (0:45 — 1:15, 30 minutes of code reading)

Open each file and locate the key functions per `EVIDENCE/github-miner.md`'s file map:

### `methods/latent_mas.py`

| Line range | Function | Read this first |
|------------|----------|-----------------|
| 17-47 | `__init__` | how the method is configured (latent_steps default = 10) |
| 52-56 | `_slice_tensor` | the tensor-slicing primitive |
| 57-72 | `_truncate_past` | **the compact step**: how the HF KV cache is pruned |
| 75-196 | `run_batch` | the HF-only batch runner (no vLLM) |
| 289-420 | `run_batch_vllm` | **the hybrid runner**: HF for latent, vLLM for text |

### `models.py`

| Line range | Function | Read this first |
|------------|----------|-----------------|
| 19-24 | `_past_length` | returns `past_kv[0][0].shape[-2]` |
| 27-67 | `ModelWrapper.__init__` | how HF + vLLM are both loaded when `use_vllm=True` |
| 230-289 | `generate_latent_batch` | the per-agent latent forward pass |
| 291-339 | `generate_latent_batch_hidden_state` | **the compact-output function** — returns embeddings AND past_kv |

**Key insight**: LatentMAS's "compact" step is NOT a separate algorithm. It's:
1. Run the HF model with `past_key_values=<accumulated cache>` on the next agent's prompt
2. Read `outputs.hidden_states[-1]` to get the latent embedding of the new tokens
3. Use `_truncate_past(outputs.past_key_values, tokens_to_keep)` to prune the KV cache to the most recent few hundred tokens for the next hop
4. Pass the pruned `past_kv` + the new embedding to the next agent

The "attention" step is the judger agent's final forward pass, which receives the **concatenation** of all prior agents' latent embeddings as a prefix — that's what the `embedding_record` + `past_embedding` variables track in `run_batch_vllm` (lines 309-315, 355-367).

**Take notes in a session scratch file** — what's the input format, what's the output format, what's the key hidden state tensor shape.

**Success criterion**: you can draw a block diagram on paper showing "agent 1 → compact → agent 2 → compact → ... → judger → answer" with the data types at each arrow (tensors, past_kv tuples, hidden states).

## Step 4 — Run the reference example (1:15 — 2:15, 1 hour)

Run LatentMAS's own example on GSM8K to verify the reference impl works on your hardware:

```bash
cd ~/PROJECTS/LatentMAS

# Smaller smoke test: 20 samples instead of the full dataset
python run.py \
    --method latent_mas \
    --model_name Qwen/Qwen3-14B \
    --task gsm8k \
    --prompt sequential \
    --max_samples 20 \
    --max_new_tokens 2048 \
    --use_vllm \
    --tensor_parallel_size 1 \
    --gpu_memory_utilization 0.85 \
    --latent_steps 10 \
    2>&1 | tee spike-run.log
```

**Watch for**:
- Model download progress (first run only, ~28GB Qwen3-14B bf16)
- vLLM server startup (~60-120 seconds)
- Each GSM8K question processed: should take ~5-30 seconds depending on latent_steps and model size
- **Wall time for 20 samples**: expect 10-20 minutes

**Collect**:
- Total wall time
- Token count (input + output) from vLLM logs
- Per-question KV cache size (from LatentMAS prints if any)
- Accuracy (% correct on the 20 samples)
- GPU memory peak (`nvidia-smi` in another terminal)

**Success criterion**: the run completes without errors, produces an accuracy number, and logs a wall-clock duration. Hitting a specific accuracy is NOT a success criterion — the goal is "the reference impl runs on my hardware."

### Failure branch: Qwen3-14B OOMs on your GPU

Fall back to Qwen3-8B or Qwen3-4B. Both are in LatentMAS's README as supported. Adjust:
```bash
--model_name Qwen/Qwen3-8B
```

### Failure branch: vLLM + HF dual-model loading fails

LatentMAS loads both vLLM and HF transformers of the same model. If this doubles VRAM and OOMs, drop `--use_vllm` and run pure-HF:
```bash
python run.py --method latent_mas --model_name Qwen/Qwen3-8B --task gsm8k \
    --prompt sequential --max_samples 20 --latent_steps 10
```
This is slower but simpler memory-wise.

## Step 5 — Measure the baseline vs latent comparison (2:15 — 3:15, 1 hour)

Run the `text_mas` baseline on the same 20 samples:

```bash
python run.py \
    --method text_mas \
    --model_name Qwen/Qwen3-14B \
    --task gsm8k \
    --prompt sequential \
    --max_samples 20 \
    --max_new_tokens 2048 \
    --use_vllm \
    --tensor_parallel_size 1 \
    --gpu_memory_utilization 0.85 \
    2>&1 | tee spike-baseline.log
```

**Collect**:
- Wall time (expected to be HIGHER than latent_mas per the paper's 4-4.3x speedup claim)
- Total token count (expected to be HIGHER, since text_mas passes natural-language messages)
- Accuracy (expected to be similar or slightly worse)

**Compute ratios**:
```
token_savings = (tokens_text_mas - tokens_latent_mas) / tokens_text_mas
wall_time_ratio = wall_time_text_mas / wall_time_latent_mas
accuracy_delta = acc_latent_mas - acc_text_mas
```

**LatentMAS published claims** (from README "LatentMAS reduces ~50-80% tokens" and "~3x-7x wall-clock time"):
- `token_savings` ∈ [0.50, 0.80]
- `wall_time_ratio` ∈ [3.0, 7.0]

## Step 6 — Go / no-go decision (3:15 — 3:45)

**GO criteria** (Akash should proceed with Hook C as a production integration):
1. The 20-sample run completed
2. `token_savings >= 0.20` (even a 20% reduction is worthwhile for Akash's multi-specialist sessions)
3. `wall_time_ratio >= 1.5` (at least 50% faster)
4. `accuracy_delta >= -0.05` (accuracy loss under 5 percentage points)
5. Memory fit: peak VRAM < 40GB (fits on a 48GB A6000 / 40GB A100 with margin)

**NO-GO criteria** (defer Hook C, file lessons):
1. Run failed repeatedly (environment issues, not solvable in the time box)
2. `token_savings < 0.05` (LatentMAS isn't helping on this task shape)
3. `accuracy_delta < -0.10` (big accuracy loss — latent handoff is destroying information)
4. Memory fit impossible (needs multi-GPU; defer)

**DEFER criteria** (inconclusive, collect more data):
1. Run completed but numbers are ambiguous (e.g., small sample size, high variance)
2. Expand to 100-200 samples IF time permits (Step 8)
3. Otherwise, file the results and decide later

## Step 7 — Write the spike report (3:45 — 4:30)

Produce `~/PROJECTS/LatentMAS/SPIKE_REPORT.md` with:

```markdown
# LatentMAS Spike — <date>

## Environment
- GPU: <model + VRAM>
- Python: <version>
- vLLM: <version>
- LatentMAS commit: <sha>
- Model used: Qwen3-<N>B

## Reference run (LatentMAS)
- Samples: 20
- Wall time: <seconds>
- Tokens: <input> input, <output> output
- Accuracy on GSM8K: <%>
- Peak VRAM: <GB>

## Baseline run (text_mas)
- Samples: 20
- Wall time: <seconds>
- Tokens: <input> input, <output> output
- Accuracy on GSM8K: <%>
- Peak VRAM: <GB>

## Ratios
- token_savings: <ratio>
- wall_time_ratio: <ratio>
- accuracy_delta: <pp>

## Verdict
- [ ] GO — proceed with Hook C production integration
- [ ] DEFER — results inconclusive, collect more data
- [ ] NO-GO — defer indefinitely, file lessons

## Blockers
- <any issues encountered>

## Lessons for retrospector
- <2-3 observations worth writing to MEMORY.md>
```

## Step 8 — (Optional) expand the run if time permits

If you're at 3:30 and everything looks good, rerun with `--max_samples 100` for a tighter confidence interval on the ratios. If not, don't bother — the 20-sample smoke test is enough for the go/no-go call at this stage.

## What the spike does NOT do

**Explicitly out of scope for the one-evening spike**:
1. **Integration with research-lead's dispatch loop**: that's a week-level engineering project, not an evening prototype. This spike measures feasibility, not builds production.
2. **Custom vLLM prefix-caching port**: the spike clones LatentMAS verbatim. Porting the KV-cache handoff to vLLM's native prefix-cache API (for long-term prod integration) is future work.
3. **Running on Akash's actual research workload**: the spike uses GSM8K because that's the reference benchmark LatentMAS uses. Research-session benchmarking requires a new task format (not available this evening).
4. **Fine-tuning latent_steps or other hyperparameters**: the spike uses the paper's defaults.

## Integration surface (for future engineering work, not this spike)

When (if) Akash graduates Hook C from spike to production, the integration surface is:

1. **Research-lead dispatches a specialist with shared context**. Currently the lead passes a natural-language brief in the dispatch message. In a LatentMAS-style integration, the lead passes a `past_key_values` handle (pointer to compact KV cache state) alongside the natural-language brief. The specialist's vLLM worker reuses the KV prefix.

2. **Research-lead writes a "shared latent working memory"** (LatentMAS terminology) that specialists can read. This replaces or supplements `EVIDENCE/*.md` for cross-specialist handoff.

3. **Specialists return their outputs as both text AND updates to the shared latent memory**. The lead's next round reads both.

This is a significant architectural change. Do not attempt in the evening spike; gate it on the spike's GO verdict.

## Alternative if the LatentMAS repo path fails

If the LatentMAS repo doesn't clone, doesn't install, or can't be made to run on Akash's hardware, the fallback spike plan is:

**Fallback Step 1**: write a minimal vLLM prefix-caching demo. Two agents take turns producing tokens, with each agent's vLLM request reusing the other agent's prefix via `enable_prefix_caching=True`.

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="Qwen/Qwen3-8B",
    enable_prefix_caching=True,
    gpu_memory_utilization=0.85,
)
sp = SamplingParams(temperature=0.7, max_tokens=256)

# Agent 1 thinks
prompt1 = "You are Agent 1. Solve this problem step by step: ..."
out1 = llm.generate([prompt1], sp)

# Agent 2 reads Agent 1's work and continues
# Note: vLLM's prefix caching is token-prefix based, not hidden-state based.
# For the same prefix bytes, vLLM reuses the KV cache automatically.
prompt2 = prompt1 + out1[0].outputs[0].text + "\nYou are Agent 2. Verify and extend: ..."
out2 = llm.generate([prompt2], sp)

# Measure: prefix cache hit rate, latency, vs two independent calls
```

**What this demonstrates**: vLLM's native prefix caching gives you **token-level** KV cache reuse for free. This is weaker than LatentMAS's **hidden-state-level** latent compact (which compresses across different natural-language expressions) but it's buildable in 1 hour and gives real data on how much of Akash's multi-agent cost is KV-cache-reusable.

**Fallback verdict**: file as "vLLM prefix caching alone is X% of the LatentMAS benefit" for a future decision.

## Confidence

**High** on the spike plan being executable in the time box. LatentMAS's repo is alive, its requirements are minimal, and its reference run on GSM8K is the paper's own reproducibility target. The go/no-go criteria are empirical ratios computed from the runs. The fallback is a reasonable plan B if the primary path fails.

## Citations

- LatentMAS repo — `github.com/Gen-Verse/LatentMAS`, retrieved 2026-04-12
- LatentMAS README — `github.com/Gen-Verse/LatentMAS/blob/main/README.md`, retrieved 2026-04-12 (paper arxiv 2511.20639, ~50-80% token savings, ~3x-7x wall-clock)
- LatentMAS code map — `EVIDENCE/github-miner.md` § "LatentMAS repository code map"
- vLLM prefix caching docs — `docs.vllm.ai/en/latest/design/automatic_prefix_caching.html` (canonical reference, not re-fetched this session)
