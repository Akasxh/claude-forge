# HYPOTHESES.md — vllm-moe-ep-routing-2026q2

Written BEFORE dispatching any specialists (per v2 Round 0 protocol).
Seeded by the lead; will be marked supported/refuted/refined by specialists.

## H1: "vLLM has caught up with SGLang on core MoE routing but still lags on all-to-all throughput"

**Shape**: vLLM in 2026-Q1 has landed the DeepSeek-V3-class routing
primitives (fused experts, grouped GEMM, top-k + shared-expert support)
but still uses a less-optimized all-to-all implementation than SGLang's
DeepEP integration. For `num_experts > tp_size` specifically, vLLM
handles it via a hybrid TP+EP scheme that works but leaves ~20-40%
throughput on the table vs SGLang in the same scenario.

**Status at Round 0**: open.

**What would refute it**: a cartographer finding that vLLM has already
integrated DeepEP, or an empiricist calculation showing the all-to-all
is a fraction of a percent of step time.

## H2: "`num_experts > tp_size` is a solved problem and all three frameworks handle it identically via EP decomposition"

**Shape**: the 2025 ecosystem converged on a near-identical recipe —
decouple EP from TP, distribute experts via a ring-like all-to-all, use
grouped-GEMM for per-rank expert batching, and scale EP independently.
vLLM, SGLang, TRT-LLM all look basically the same at the MoE layer now.
The "prioritization" question is a non-question; pick the framework by
non-MoE criteria (scheduler, KV cache, client API).

**Status at Round 0**: open — this is the "null hypothesis" — if true,
Akash's question doesn't resolve to "which PR to file", it resolves to
"none, MoE routing is done, work on something else".

**What would refute it**: any substantive architectural difference
between frameworks revealed by cartographer / librarian, or any benchmark
showing > 10% throughput spread on the same model.

## H3: "The real bottleneck isn't routing, it's the expert dispatch + combine all-to-all, and DeepEP / ep_kernels are the load-bearing innovation"

**Shape**: The interesting work in 2025 wasn't routing-algorithm work —
it was making the expert-parallel all-to-all not suck. DeepSeek released
DeepEP as part of their open-source week; NVIDIA TRT-LLM has its own
kernels; SGLang integrated DeepEP; vLLM is either in-progress or has
its own implementation. The contribution question reduces to: which
framework has the largest gap in its expert-dispatch kernel pipeline
and can accept a PR from a new contributor?

**Status at Round 0**: open — if true, Akash's highest-leverage PR is
almost certainly on the kernel/all-to-all side, not on the routing
algorithm side.

**What would refute it**: a finding that all frameworks already ship
kernels within 5% of each other, leaving no gap.

## H4: "DeepSeek-V3/V4 routing is only one design point — the 2026 frontier is elastic/dynamic EP and models with `num_experts` much larger than was common in 2024-2025 (1024+ experts like Qwen-3-MoE), which breaks assumptions in all three frameworks"

**Shape**: The 2025 DeepSeek-V3 wave set a template around 256 experts.
The 2026 Qwen3-MoE / Llama-4 MoE / deepseek v4 generation has blown
that up: 1024+ experts, dynamic top-k, and per-layer expert counts.
None of vLLM / SGLang / TRT-LLM is cleanly designed for this, and all
three are rushing to catch up in 2026-Q1. This is where the new-contributor
leverage actually is.

**Status at Round 0**: open — depends heavily on what models are actually
in production today. If this is speculation about a model that doesn't
exist yet, it's noise.

**What would refute it**: no such models in prod, no such PRs in flight.

## Pre-registered bias warnings

- The lead (me) has a soft prior toward H3 because it's the most
  satisfying "narrative." That's a confirmation-bias smell. Skeptic
  must attack H3 especially hard.
- The "new contributor should prioritize X" question is prone to
  recency bias (whatever shiny PR landed last week feels most
  important). Archaeologist should check PR velocity over a year,
  not a week.
- H4 is partially my own speculation. Historian must source every
  claim about 2026 Qwen3-MoE / Llama-4 MoE / DeepSeek-V4 independently
  or the hypothesis must be downgraded to "speculative" in SYNTHESIS.md.
