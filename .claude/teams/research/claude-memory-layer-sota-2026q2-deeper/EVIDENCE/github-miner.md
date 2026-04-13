# GitHub-Miner — LatentMAS code map + ByteRover blueprint + repo audits

Sub-question: map the LatentMAS repo in file-path-exact detail so the Hook C spike plan names functions by line number; verify ByteRover CLI as a real production-grade reference; audit the pilot-cited competitor repos (Mem0, Letta, Graphiti, MemPalace, MemX) for any 14-day commits that change the recommendation.

## Method

- WebFetched `github.com/Gen-Verse/LatentMAS` repo overview + `methods/latent_mas.py`, `methods/text_mas.py`, `run.py`, `requirements.txt`, `models.py` + commits page
- WebFetched `github.com/campfirein/byterover-cli` + `docs.byterover.dev`
- WebFetched commits pages for Letta, Mem0, Graphiti, MemPalace (2026-03-29 through 2026-04-12 window)
- WebFetched `github.com/memxlab/memx` for reference ranker values

## LatentMAS repository code map

**Repository**: `Gen-Verse/LatentMAS`
**Stars**: 868 (2026-04-12)
**Last substantive commit**: `55d6e55` on 2026-02-09 ("Update new extensions of LatentMAS")
**Last README commit**: `b9b2095` on 2026-03-27
**License**: inferred OSS; LICENSE file present (not fetched verbatim; confirmed present in tree listing)
**Open issues**: 12; open PRs: 3
**Python version**: 3.10 (per README `conda create -n latentmas python=3.10`)

### File tree (top level, from WebFetch 2026-04-12)

```
LatentMAS/
├── assets/                  # images for README (main_table1.png, etc.)
├── data/                    # task datasets (loaders for GSM8K, AIME, etc.)
├── example_logs/            # sample run outputs
├── methods/                 # method implementations (critical for Hook C)
│   ├── baseline.py          # single-agent baseline
│   ├── text_mas.py          # text-message-passing multi-agent system
│   └── latent_mas.py        # ← compact-then-attend implementation
├── __init__.py
├── data.py                  # dataset dispatch
├── models.py                # ← ModelWrapper class (KV cache handoff)
├── prompts.py               # prompt templates
├── run.py                   # entry point (argparse, method dispatch)
├── utils.py                 # helpers
├── requirements.txt
├── LICENSE
└── README.md
```

### Critical file #1: `methods/latent_mas.py`

Size: ~420 lines. Key functions:

| Function | Line range | Purpose |
|----------|------------|---------|
| `__init__(self, model: ModelWrapper, *, latent_steps: int = 10, ...)` | 17-47 | Configure the method with a model and the number of latent steps per agent |
| `_slice_tensor(tensor, tokens_to_keep)` | 52-56 | Static helper: slice along the sequence dim |
| `_truncate_past(self, past_kv, tokens_to_keep)` | 57-72 | **Core of the compact step.** Slices the HuggingFace `past_key_values` tuple to a shorter length so only the relevant KV-cache prefix is retained |
| `run_batch(self, items: List[Dict])` | 75-196 | Transformers-backend batch runner (HF generate loop) |
| `run_batch_vllm(self, items: List[Dict])` | 289-420 | **vLLM-backend batch runner.** Inside this method: lines 309-315 build the embedding record list; 355-367 call `generate_latent_batch_hidden_state` (on the HF model, not vLLM, for the latent step); attention fuses concatenated latent embeddings before judger dispatch |
| `run_item(self, item: Dict)` | 422-423 | Single-item convenience wrapper |

**Key imports** (lines 1-15 area):
```python
from models import ModelWrapper, _past_length
from vllm import SamplingParams
import torch
from transformers.cache_utils import Cache  # conditional import
```

**Critical architectural fact**: `latent_mas.py` uses **HuggingFace Transformers' `past_key_values`** format (via `transformers.cache_utils.Cache`) for the compact-then-attend pattern. The vLLM backend is ONLY used for the final text generation step — vLLM's PagedAttention / prefix-caching API is **NOT** the KV-cache handoff mechanism. The handoff happens in HuggingFace land via tensor slicing on the `past_key_values` tuple.

**Implication for Hook C**: if Akash wants to do this in production with his vLLM setup, he has two choices:
1. **Clone LatentMAS's approach verbatim**: run the latent step on HF Transformers (not vLLM) and use vLLM only for text generation. This is what the reference impl does.
2. **Port to vLLM's native prefix-caching API**: read/write the KV cache via vLLM's `LLMEngine.generate` with `prefix_cache_id`. This is NOT what LatentMAS does and would require novel code.

**The one-evening spike MUST be option 1** — clone LatentMAS and reproduce their reference result on a known benchmark. Porting to vLLM's native API is a week-level project at minimum.

### Critical file #2: `models.py`

Key class and methods:

| Symbol | Line range | Purpose |
|--------|------------|---------|
| `_past_length(past_kv)` | 19-24 | Returns `past_kv[0][0].shape[-2]` — the cached sequence length from a HF tuple |
| `class ModelWrapper: __init__` | 27-67 | Initializes with both HF transformers and optional vLLM. When `use_vllm=True`, it maintains BOTH a vLLM `LLM` instance AND a fallback HF `AutoModelForCausalLM` for the latent path |
| `generate_text_batch(..., past_key_values=None)` | 168-203 | HF text generation with optional KV prefix continuation |
| `generate_latent_batch(..., latent_steps=10)` | 230-289 | Runs `latent_steps` forward passes producing latent representations, returns new `past_kv` |
| `generate_latent_batch_hidden_state(...)` | 291-339 | **The compact step.** Returns concatenated embedding outputs + the KV-cache past states |
| `vllm_generate_text_batch(...)` | ? | Text generation via vLLM's `LLM.generate` for the final judger phase |

**Key imports** (lines 1-18):
```python
import os
import csv
import torch
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    from vllm import LLM, SamplingParams
    _HAS_VLLM = True
except ImportError:
    _HAS_VLLM = False
```

**The two-backend design**: `ModelWrapper.__init__` loads both a vLLM server AND a HuggingFace `AutoModelForCausalLM` when `use_vllm=True`. vLLM handles the large-batch text output (faster throughput); HF handles the per-token latent hidden-state extraction (vLLM doesn't expose hidden states through its generate API as of this writing).

### Critical file #3: `run.py`

Entry point (argparse). Key arguments:

```python
--method {baseline, text_mas, latent_mas}         # required
--model_name <Qwen variant>                       # required (paper uses Qwen3-14B)
--task {gsm8k, aime2024, aime2025, gpqa, 
        arc_easy, arc_challenge, mbppplus, 
        humanevalplus, medqa}
--prompt {sequential, hierarchical}
--max_samples -1                                  # -1 = all
--max_new_tokens 4096                             # default
--latent_steps 10                                 # LatentMAS specific
--temperature, --top_p                            # generation
--generate_bs                                     # batch size
--device                                          # GPU
--split test                                      # default dataset split
--use_vllm                                        # flag to enable vLLM backend
--enable_prefix_caching                           # vLLM-specific
--tensor_parallel_size                            # vLLM-specific
--gpu_memory_utilization                          # vLLM-specific
```

**Import dispatch**:
```python
from methods.baseline import BaselineMethod
from methods.text_mas import TextMASMethod
from methods.latent_mas import LatentMASMethod
from models import ModelWrapper
```

### Requirements.txt (verbatim)

```
transformers
torch
numpy
tqdm
accelerate
datasets
```

**Notable**: vLLM is NOT in requirements.txt; it's optional (`pip install vllm` separately). This confirms vLLM is a secondary optimization, not the core of the method.

## ByteRover CLI — production-grade reference

**Repository**: `github.com/campfirein/byterover-cli`
**Stars**: **4,400** (as of 2026-04-12)
**Former name**: Cipher (README notes it's "formerly Cipher")
**License**: **Elastic License 2.0** (commercial-source-available, NOT OSS-compatible for commercial redistribution)
**Language**: TypeScript (with React/Ink for TUI)
**Install**: `curl -fsSL https://byterover.dev/install.sh | sh` or `npm install -g byterover-cli`
**Node minimum**: >= 20
**Commits on main**: 2,647 commits (high velocity)

### Integration surface

**AI agents supported** (22+): Cursor, Claude Code, Windsurf, Cline, etc.
**MCP server**: exposed via `brv mcp` command
**CLI commands**:
- `/curate` — add knowledge to the context tree
- `/query` — retrieve from the context tree (5-tier progressive retrieval)
- `brv curate view` — inspect history
- `brv review {pending,approve,reject}` — curation workflow (echoes the ACE curator role)

### On-disk layout (per docs.byterover.dev and § 3.2 of the paper)

```
<project>/.brv/context-tree/
├── <domain>/                    # e.g. "engineering", "research"
│   ├── <topic>/                 # e.g. "vllm-optimization"
│   │   └── <entry>.md           # markdown with YAML frontmatter
```

### Frontmatter schema (per § Appendix C of the paper)

```yaml
---
title: <str>
tags: [<str>, ...]
keywords: [<str>, ...]
related: [<rel-path>, ...]   # @-annotations for explicit edges
importance: 0-100            # AKL score
maturity: draft|validated|core
recency: 0.0-1.0             # exp(-Δt/30)
accessCount: <int>
updateCount: <int>
timestamps:
  created: <ISO>
  last_accessed: <ISO>
  last_updated: <ISO>
---
```

**Critical take**: ByteRover's `<domain>/<topic>/<entry>.md` hierarchy is **slightly different** from Claude Code's flat `~/.claude/agent-memory/<agent>/<topic>.md`. ByteRover nests; Claude Code is flat. For Hook A, Akash should use the **flat Claude Code convention**, not ByteRover's nested hierarchy, because:
1. Claude Code's auto-injection machinery reads the flat MEMORY.md + flat topic files.
2. Nested subdirectories break the standard-file-tools discovery (lead would need to `find` or `glob` recursively).
3. The Research Team has ~10-30 topics total — a flat namespace is tractable.

Akash's Hook A DOES adopt:
- ByteRover's AKL formula (`+3` access, `+5` update, `*0.995` daily)
- ByteRover's maturity tiers with hysteresis (draft/validated/core)
- ByteRover's YAML frontmatter schema (for topic files)

Akash's Hook A does NOT adopt:
- ByteRover's nested directory hierarchy (use flat per Claude Code convention)
- ByteRover's CLI binary (keep Akash's existing scribe agent behavior)
- ByteRover's 5-tier retrieval (Akash's session-start auto-injection + on-demand file read is tier 0 and tier 2-4 collapsed; a full 5-tier engine is Hook B's job, not Hook A's)

## Competitor commit audit (2026-03-29 through 2026-04-12)

### Mem0 (`mem0ai/mem0`)
- 2026-04-12 `c239d8a` — client telemetry TypeError fix
- 2026-04-12 `9d6b79a` — remove enable_graph flag, camelCase
- 2026-04-11 `9d82e23` — PostHog sampling at 10% (telemetry volume)
- 2026-04-06 `4c2db3e` — Mem0 skill graph with CLI
- **No benchmark methodology corrections.** **No response to Zep rebuttal.** The `4c2db3e` "skill graph" commit is a new feature, not an audit response.
- **Adversary classification unchanged**: MIXED, contested benchmarks.

### Letta (`letta-ai/letta`)
- 2026-04-08 `bb52a89` — workflows update
- 2026-04-07 `f1800c8` — anti-spam issue guard
- 2026-04-07 `c71353f` — issue guard AI disclosure policy
- 2026-03-31 `f0364bc` — **"Update summarizer prompt to remember plan files, github PRs, etc."** (SUBSTANTIVE: extends the summarizer's memory to reference plan files + gh PRs — this is convergent with Hook A's topic-file routing direction)
- 2026-03-31 `54c346f` — `MemfsClient` fix (MemFS backend, still maintained)
- 2026-03-31 `f333247` — version bump 0.16.7
- **Letta is convergent** with the ACE-pattern direction. No architecture changes; maintenance-mode for the Context Repositories feature.
- **Classification unchanged**: HEALTHY, valid fallback for the curator role.

### Graphiti (`getzep/graphiti`)
- 2026-04-05 `3630e343` — CLA signatures
- 2026-04-04 `9e93426b` — CLA signatures
- 2026-04-03 `221cae4c` — "Remove OIDC perms and add Claude allowlist comments"
- 2026-04-02 `b24b9b34` — "Pin GitHub Actions to commit SHAs for security" (co-authored with Claude)
- 2026-04-02 `58d9da38` — "Refined slop detection and triage comments"
- **No bi-temporal validity changes.** **No core architecture work.** Routine maintenance + security hardening.
- **Classification unchanged**: MIXED (technical critique of Mem0 still valid, self-reported LoCoMo numbers still on saturated benchmark).

### MemPalace (`milla-jovovich/mempalace`)
- **No code commits** fixing the benchmark fraud since maintainer's 2026-04-09 acknowledgment
- **New issues 2026-04-11**: #649 ("Hidden network dependency violates offline-first guarantees", bug, geovanirz) — a second methodology violation (the project claims offline-first but makes network calls). #650 ("Windows setup failures"), #648 (docs site request), #646 (JSON parser bug), #645 (--refresh flag request)
- **Classification unchanged**: REJECTED. The 2026-04-11 #649 finding is a new red flag — on top of benchmark fraud, the offline-first claim is also false.

### MemX (`memxlab/memx`)
- Only 2 commits total, 2 stars. This is a "reference dump" repo — the paper (arxiv 2603.16171) is the primary source, not the repo. The commented-out config in the README gives the weight values (`semantic_weight = 0.45`, `recency_weight = 0.25`, `importance_weight = 0.10`, `frequency_weight = 0.05`).
- **Classification**: paper is STRONG-PRIMARY; repo is low-trust, do not adopt code.

### LatentMAS (`Gen-Verse/LatentMAS`)
- 2026-03-27 `b9b2095` README
- 2026-03-26 `c2fea01` README
- 2026-02-27 `c14da9c` README
- 2026-02-09 `55d6e55` — **"Update new extensions of LatentMAS"** (last code change)
- 2026-02-07 PR #35 merged — "Awareness Network" item
- **Classification unchanged**: STRONG-PRIMARY (paper arxiv 2511.20639 + real code). Repo is alive; clone-ready for Hook C spike.

## Handoff

- **empiricist** — use the LatentMAS file map to scope the one-evening spike (clone + hello-world + latency measurement)
- **linguist** — the ByteRover frontmatter schema + AKL vocabulary should be absorbed into the scribe heuristic
- **skeptic** — attack: is ByteRover CLI a "just adopt this instead" argument? (Answered in skeptic.md: no, because the license is Elastic, the layout is nested, and the MCP surface would replace Akash's existing scribe — higher operational delta than Hook A.)

## Confidence

**High**. Every line-number citation is from direct WebFetch of the raw file. Every commit citation is from the repo's commits page. Every star count is from the repo overview. No tool-chain errors.

## Citations

- LatentMAS repo — `github.com/Gen-Verse/LatentMAS`, retrieved 2026-04-12
- LatentMAS `latent_mas.py` — `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/methods/latent_mas.py`, retrieved 2026-04-12
- LatentMAS `text_mas.py` — `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/methods/text_mas.py`, retrieved 2026-04-12
- LatentMAS `models.py` — `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/models.py`, retrieved 2026-04-12
- LatentMAS `run.py` — `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/run.py`, retrieved 2026-04-12
- LatentMAS `requirements.txt` — `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/requirements.txt`, retrieved 2026-04-12
- LatentMAS commits — `github.com/Gen-Verse/LatentMAS/commits/main`, retrieved 2026-04-12
- ByteRover CLI — `github.com/campfirein/byterover-cli`, retrieved 2026-04-12
- ByteRover docs — `docs.byterover.dev`, retrieved 2026-04-12
- ByteRover paper — `arxiv.org/html/2604.01599`, retrieved 2026-04-12
- Mem0 commits — `github.com/mem0ai/mem0/commits/main`, retrieved 2026-04-12
- Letta commits — `github.com/letta-ai/letta/commits/main`, retrieved 2026-04-12
- Graphiti commits — `github.com/getzep/graphiti/commits/main`, retrieved 2026-04-12
- MemPalace issues — `github.com/milla-jovovich/mempalace/issues?q=is%3Aissue+updated%3A%3E2026-04-08`, retrieved 2026-04-12
- MemX repo — `github.com/memxlab/memx`, retrieved 2026-04-12
