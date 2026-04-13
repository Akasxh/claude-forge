# Parametric phase — LoRA distillation data spec + training recommendation

This file defines the 6-month parametric direction in implementation-grade detail. The forthcoming Engineering Team will use it to build the distillation pipeline when the trigger conditions are met.

## Decision summary

- **Model**: **Qwen3-8B** (base, not instruct — tune to the specific research-lead voice)
- **LoRA rank**: **16**, target modules `q_proj k_proj v_proj o_proj gate_proj up_proj down_proj`
- **Format**: supervised instruction tuning (SFT) with synthetic paraphrased prompts
- **Dataset target**: 300-500 stable lessons → 1,500-2,500 training pairs
- **Stability gate**: `reinforced_by_count >= 3 AND maturity >= validated AND days_since_creation >= 30`
- **Training time**: ~45-90 minutes on 1x 4090 (or 20-40 minutes on H100)
- **Eval**: 2-part (lesson recall + capability regression)
- **Trigger**: when the scribe's stability counter reports ≥300 eligible lessons
- **Timeline to trigger**: ~4-6 years solo; ~12-18 months with 5 active teams

See `EVIDENCE/empiricist.md` § "LoRA distillation scope and sizing" and `EVIDENCE/historian.md` § "LoRA minimum dataset size prior art" for derivation.

## What exactly gets distilled

### Input: stable lessons from MEMORY.md

A lesson is stable and eligible if:
- `reinforced_by_count >= 3` — it was cited in 3+ distinct session retrospectors
- `maturity >= validated` — it passed the ByteRover AKL threshold (importance ≥ 65, see Hook A)
- `days_since_creation >= 30` — not a flash-in-the-pan observation

The scribe maintains the `reinforced_by` field as a list of session slugs. At distillation time, a small filter script reads MEMORY.md + the scribe's topic files and emits the eligible subset.

### NOT distilled

- **Raw SYNTHESIS.md files** — too session-specific, would encode false generalizations
- **EVIDENCE files** — case-specific, not rules
- **Failed hypotheses** — contradicted lessons; would poison the model
- **Lessons marked `Stale?` or `Superseded by N`** — also poison candidates
- **Session logs** — noise

### Shape of a training pair

Each eligible lesson produces 3-5 synthetic instruction/response pairs. Example for the lesson "The skeptic attacks reasoning; the adversary attacks the corpus":

```jsonl
{"instruction": "You are running a research investigation on a topic with significant web/community sources. Which specialists should you dispatch for the adversarial gates?", "output": "Dispatch both the skeptic (attacks the synthesis from inside — checks if the claims follow from the sources) AND the adversary (attacks the corpus from outside — checks if the sources are fraudulent or SEO-gamed). Skeptic alone is insufficient for web-heavy investigations because it cannot see benchmark fraud or citation laundering."}
{"instruction": "A specialist just returned a web-sourced claim about a recent benchmark number. Does the skeptic's gate alone suffice before marking 'high confidence'?", "output": "No. The skeptic verifies that the synthesis faithfully represents the source, but cannot verify that the source itself is honest. For any web-sourced benchmark claim, the adversary gate is mandatory before high confidence — the adversary checks source quality, fraud patterns, and independent reproduction."}
{"instruction": "What is the division of labor between research-skeptic and research-adversary?", "output": "Skeptic attacks reasoning — unstated assumptions, competing hypotheses, synthesis-internal logic. Adversary attacks corpus — source quality, SEO farms, celebrity attribution, benchmark fraud, citation laundering. Both gates are required for high confidence when the evidence base includes web or community sources."}
```

**Prompt construction**: the instruction is a paraphrased question that a reasonable user or a dispatching lead might ask. The output is the rule of thumb and its rationale, in the lead's voice.

### Synthetic prompt generator

A small Python script at `~/.claude/distillation/synth.py` (speculative path; path is the Engineering Team's call):

```python
"""Generate synthetic instruction tuning pairs from stable MEMORY.md lessons."""
import json
import re
from pathlib import Path
from anthropic import Anthropic  # or any frontier model client

PARAPHRASE_SYSTEM_PROMPT = """You are generating supervised fine-tuning data.
Given a single lesson from a research-lead agent's MEMORY.md playbook,
produce exactly 4 JSONL-format instruction/output pairs. Each pair should
paraphrase the lesson from a different angle:

1. A direct "what rule applies to situation X" question.
2. A "when should I do Y" procedural question.
3. A "why is Z the rule" rationale question.
4. An "is it true that..." verification question.

Each output should deliver the rule of thumb plus its concise rationale,
in first-person research-lead voice. Do not invent facts beyond the lesson.
Output only the JSONL, one pair per line, no preamble."""

client = Anthropic()

def extract_lessons(memory_md: str) -> list[dict]:
    """Parse MEMORY.md into lesson dicts."""
    # ... parser that splits on '### Lesson N —' headers
    # ... filters to lessons with stability fields satisfied
    ...

def paraphrase(lesson_text: str) -> list[dict]:
    """Call Claude Opus to produce 4 paraphrases."""
    resp = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=PARAPHRASE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": lesson_text}],
    )
    lines = resp.content[0].text.strip().split("\n")
    return [json.loads(line) for line in lines if line.startswith("{")]

def build_dataset(memory_md: Path, out_path: Path) -> None:
    lessons = extract_lessons(memory_md.read_text())
    stable = [l for l in lessons if is_stable(l)]
    pairs = []
    for lesson in stable:
        pairs.extend(paraphrase(lesson["body"]))
    with out_path.open("w") as f:
        for pair in pairs:
            f.write(json.dumps(pair) + "\n")

def is_stable(lesson: dict) -> bool:
    return (
        lesson.get("reinforced_by_count", 0) >= 3
        and lesson.get("maturity", "draft") in ("validated", "core")
        and lesson.get("days_since_creation", 0) >= 30
    )

if __name__ == "__main__":
    build_dataset(
        Path("~/.claude/agent-memory/research-lead/MEMORY.md").expanduser(),
        Path("~/.claude/distillation/train.jsonl").expanduser(),
    )
```

**Cost of the synthesis step**: 300 lessons × 4 paraphrases × ~500 output tokens ≈ 600K tokens at Claude Opus rates ≈ $9 at current pricing. A one-time cost, run when the distillation pipeline triggers.

## Training configuration

### Hardware profile

- **Minimum**: 1x RTX 4090 (24GB) with bnb 4-bit base quantization
- **Comfortable**: 1x A100 40GB or H100 80GB with bf16 base
- **Unnecessary**: multi-GPU (the dataset is too small to benefit)

### Hyperparameters

```yaml
model: Qwen/Qwen3-8B          # base, not instruct
quantization: 4bit_bnb         # fits 4090
dtype: bfloat16
gradient_checkpointing: true

lora:
  r: 16
  alpha: 32
  dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  num_train_epochs: 3
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 2
  learning_rate: 5e-5
  lr_scheduler_type: cosine
  warmup_steps: 100
  optim: adamw_8bit
  weight_decay: 0.01
  max_seq_length: 2048
  packing: false              # each pair as its own sample
  dataset_text_field: null    # use formatting_func
  
eval:
  eval_steps: 100
  save_steps: 200
  save_total_limit: 3

logging:
  report_to: [tensorboard]
  logging_steps: 10
```

### Framework choice

**Option A: TRL SFTTrainer (recommended)**. Battle-tested, minimal code, supports PEFT/LoRA out of the box. `pip install trl peft accelerate transformers bitsandbytes`.

**Option B: Axolotl**. YAML-driven, more features, but heavier setup. Good if Akash wants to iterate on many configs.

**Option C: Unsloth**. Fastest training (~2x speedup over TRL), but adds custom kernels that occasionally break on new transformer versions.

**Recommendation**: TRL for the first run. Switch to Unsloth if training time is a bottleneck (which at 45-90 min per run, it isn't).

### Training script sketch (`~/.claude/distillation/train.py`)

```python
"""LoRA SFT of Qwen3-8B on the distilled research-lead playbook."""
import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
import torch

MODEL = "Qwen/Qwen3-8B"
DATA = "~/.claude/distillation/train.jsonl"
OUT = "~/.claude/distillation/lora-out"

def format_example(example):
    """Convert a JSONL pair into Qwen chat format."""
    return {
        "text": (
            f"<|im_start|>system\nYou are research-lead, a research investigation agent.<|im_end|>\n"
            f"<|im_start|>user\n{example['instruction']}<|im_end|>\n"
            f"<|im_start|>assistant\n{example['output']}<|im_end|>"
        )
    }

def load_dataset(path: str) -> Dataset:
    with open(path) as f:
        rows = [json.loads(line) for line in f]
    return Dataset.from_list(rows).map(format_example)

def main():
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, quantization_config=bnb, device_map="auto", trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    lora_cfg = LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        bias="none", task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    ds = load_dataset(DATA)
    split = ds.train_test_split(test_size=0.1, seed=42)

    sft_cfg = SFTConfig(
        output_dir=OUT,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        learning_rate=5e-5,
        lr_scheduler_type="cosine",
        warmup_steps=100,
        optim="adamw_8bit",
        weight_decay=0.01,
        max_seq_length=2048,
        bf16=True,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=3,
        eval_strategy="steps",
        eval_steps=100,
        logging_steps=10,
        report_to=["tensorboard"],
    )

    trainer = SFTTrainer(
        model=model, args=sft_cfg,
        train_dataset=split["train"], eval_dataset=split["test"],
        tokenizer=tokenizer,
    )
    trainer.train()
    trainer.save_model(OUT + "/final")

if __name__ == "__main__":
    main()
```

## Deployment — how the LoRA becomes usable

### Serve via vLLM with LoRA adapters

vLLM supports dynamic LoRA loading. Akash can serve the base Qwen3-8B with the distilled LoRA attached:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-8B \
    --enable-lora \
    --lora-modules research-lead-playbook=/home/akash/.claude/distillation/lora-out/final \
    --max-loras 4 \
    --max-lora-rank 16 \
    --max-cpu-loras 4
```

Requests specify `model="research-lead-playbook"` to route through the adapter.

### Or merge and serve as a new model

Alternative: merge the LoRA into the base weights and serve as a standalone model:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B", torch_dtype="bfloat16")
lora = PeftModel.from_pretrained(base, "~/.claude/distillation/lora-out/final")
merged = lora.merge_and_unload()
merged.save_pretrained("~/.claude/distillation/qwen3-8b-research-lead")
```

Then serve the merged model via vLLM normally.

**Recommendation**: LoRA-serving (Option A) is cleaner for iteration — can swap adapters without reloading the base. Merged (Option B) is better for production where the base is stable.

## Evaluation

### Part 1: lesson recall (did the LoRA encode the rules?)

Build a held-out evaluation set of 30 paraphrased questions, each tied to one specific training lesson. For each question:

1. Query the LoRA-adapted model with the question
2. Grade whether the response contains the rule of thumb (keyword check OR LLM-as-judge)
3. Target: ≥24 / 30 correct (80% recall)

**Auto-grading script**:

```python
"""Lesson recall evaluation."""
import json
from vllm import LLM, SamplingParams

LLM_JUDGE_PROMPT = """A test question about a research-agent rule and its answer.
The expected rule of thumb is below. Score 1 if the answer contains the rule's
substance, 0 otherwise. Output only 0 or 1.

Expected rule: {rule}
Question: {question}
Answer: {answer}
Score: """

llm_target = LLM(model="Qwen/Qwen3-8B", enable_lora=True, ...)
sp = SamplingParams(temperature=0.3, max_tokens=300)

with open("~/.claude/distillation/eval-recall.jsonl") as f:
    eval_set = [json.loads(line) for line in f]

correct = 0
for ex in eval_set:
    resp = llm_target.generate([ex["question"]], sp)
    answer = resp[0].outputs[0].text
    # Call LLM-as-judge (Claude Opus or the target model itself)
    judge_prompt = LLM_JUDGE_PROMPT.format(rule=ex["expected_rule"], question=ex["question"], answer=answer)
    judge_resp = anthropic_client.messages.create(model="claude-opus-4-6", ...)
    score = int(judge_resp.content[0].text.strip())
    correct += score

print(f"Recall: {correct}/{len(eval_set)} = {correct/len(eval_set):.1%}")
```

### Part 2: capability regression (did the LoRA damage the base model?)

Run a short regression battery comparing the LoRA-adapted model against the base Qwen3-8B:

| Benchmark | Samples | Base target | LoRA target | Tolerance |
|-----------|---------|-------------|-------------|-----------|
| GSM8K (math) | 50 | base score | base − 5pp | ±5% |
| HumanEval (code) | 50 | base score | base − 5pp | ±5% |
| MMLU (knowledge) | 100 subset | base score | base − 3pp | ±3% |
| IFEval (instruction following) | 50 | base score | base − 5pp | ±5% |

**Total**: 250 evaluations ≈ 1 hour on a local vLLM. Automatable via `lm-evaluation-harness` with `--model vllm` backend.

**If any benchmark regresses beyond tolerance**:
- **Option 1**: reduce LoRA rank (16 → 8) and retrain
- **Option 2**: reduce epochs (3 → 2) 
- **Option 3**: inspect the training data for noise (bad paraphrase pairs)
- **Option 4**: abandon distillation — file a lesson that LoRA distillation at this scale doesn't work for this task family

### Reporting

Produce `~/.claude/distillation/EVAL_REPORT.md` with:
- Recall: X/30
- Regression: per-benchmark delta
- Verdict: DEPLOY / TUNE / ABANDON

## Decay gate re-visited

The decay gate filters WHICH lessons get distilled. It does NOT filter when to retrain. Retraining cadence:

- **Monthly** (proposed): retrain if any new lessons have crossed the stability threshold in the last month AND the count of new stable lessons >= 10
- **Quarterly**: if monthly is too aggressive, retrain every 3 months if ≥25 new stable lessons
- **Never**: if the rate of new stable lessons is <5/month, the parametric layer isn't earning its keep — stay with token-level

**Akash's rate (observed)**: ~1 new lesson every 2-3 sessions × ~2-3 sessions/week = ~0.3-0.5 new lessons/week × 30 days/month × (1 stable / ~3 lessons mature at 30 days) ≈ **3-5 new stable lessons per month**.

**Implication**: at solo pace, Akash would hit the quarterly retrain threshold (25) in **5-8 months**. Monthly (10) in 2-3 months. This is the earliest the parametric phase becomes viable.

**With 5 teams**, the rate multiplies by ~5 (assuming similar per-team rates), so monthly becomes viable in 2-3 weeks and quarterly (25 × 5 = 125 new stable lessons) becomes viable in 2-3 months.

**Conclusion**: the parametric phase becomes reasonable after ~6 months of multi-team operation. Sooner if Akash shortens the 30-day decay gate (risk: less stable lessons poisoning the LoRA) or lowers the reinforcement threshold (same risk).

## Failure modes and mitigations

### P1: LoRA encodes contradicted lessons
**Cause**: a new lesson contradicts an old one; both are stable; both get distilled.
**Blast radius**: the LoRA outputs internally contradictory rules. Lead behavior becomes unpredictable.
**Mitigation**: during dataset build, run a contradiction check. For each lesson pair, ask a judge LLM: "do these rules contradict?" If YES, keep only the NEWER lesson in the distillation set (staleness-wins heuristic).
**Detection**: evaluator catches contradictory outputs during the recall test.

### P2: LoRA encodes session-specific detail as a generalization
**Cause**: a lesson includes a specific slug or date ("in the claude-memory-layer session, X happened"); paraphrases hallucinate generalizations from it.
**Blast radius**: LoRA spits out session-specific facts as if they were rules.
**Mitigation**: the paraphrase system prompt explicitly forbids inventing facts beyond the lesson. The distillation preprocessing strips session slugs and specific dates from the lesson body before paraphrasing.
**Detection**: manual inspection of 20 random paraphrases before training.

### P3: LoRA poisons base model capability
**Cause**: over-training, too-high LoRA rank, or noisy training data.
**Blast radius**: the deployed worker fails on capability benchmarks.
**Mitigation**: Part 2 of the evaluation catches this. Tolerance bands are generous to allow some degradation but block catastrophic loss.
**Detection**: capability regression eval.

### P4: Distilled LoRA goes stale fast
**Cause**: a lesson was stable at distillation time but became wrong soon after. The weights now encode a wrong rule.
**Blast radius**: the worker applies an outdated rule with confidence.
**Mitigation**: 
1. Monthly/quarterly retraining cadence (see above)
2. Between retrains, new lessons still live in MEMORY.md and the lead reads them at session start — token-level overrides weight-level
3. If a lesson explicitly supersedes a previously-distilled one, flag it HIGH-PRIORITY for the next retrain

## Confidence

**Medium-high** on the architectural choices (Qwen3-8B, rank 16, SFT format). These are canonical for the task.

**Medium** on the timing (4-6 years solo, 12-18 months with teams) — extrapolated from current lesson accumulation rate.

**Medium-low** on the specific recall numbers expected — no published benchmark for "agent playbook distilled into a small LoRA" that matches Akash's exact task family. The eval criteria are REASONABLE but UNTESTED against Akash's workload.

## Handoff

- **IMPLEMENTATION_SEQUENCE** — parametric is the last phase (steps 19-22), gated on accumulated lesson count
- **retrospector** — lesson to add: "Parametric memory is not on this quarter's critical path; the timeline is multi-year solo, ~year-long with teams. Don't over-invest before the lesson count supports it."
- **skeptic** — attack: is SFT the right format? (SFT for MVP; DPO deferred to v2 — see Attack 5 in skeptic.md. The MVP does NOT use DPO because Akash lacks preference data. v2 DPO upgrade becomes viable once real preference pairs accumulate from MVP LoRA deployment — e.g. sessions where the LoRA-backed worker gives answer X but the correct answer is Y, logged by the scribe or the evaluator.)
- **moderator** — no open debate

## Citations

- LIMA paper (minimum dataset size rule) — `arxiv.org/abs/2305.11206`, 2023
- Unsloth docs — `unsloth.ai/docs/get-started/fine-tuning-llms-guide`, retrieved 2026-04-12
- distil-labs benchmark (Qwen3 top of small-model fine-tune leaderboard) — `distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/`, retrieved 2026-04-12
- TRL SFTTrainer — `huggingface.co/docs/trl/sft_trainer` (canonical, not re-fetched)
- PEFT LoRA — `huggingface.co/docs/peft/developer_guides/lora` (canonical)
- bitsandbytes 4-bit quantization — `github.com/bitsandbytes-foundation/bitsandbytes` (canonical)
- vLLM dynamic LoRA serving — `docs.vllm.ai/en/latest/models/lora.html` (canonical)
- ByteRover AKL formula (for stability gating) — `arxiv.org/html/2604.01599` § 3.2.3, retrieved 2026-04-12
- Akash's observed lesson rate — `~/.claude/agent-memory/research-lead/MEMORY.md`, 9 lessons over observed session timespan (2026-04-12 snapshot)
