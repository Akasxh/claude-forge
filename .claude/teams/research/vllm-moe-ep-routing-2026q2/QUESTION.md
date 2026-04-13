# QUESTION.md — vllm-moe-ep-routing-2026q2

## Raw prompt (verbatim)

> How should vLLM handle MoE expert-parallel (EP) routing for models where
> expert count exceeds the tensor-parallel world size, and how does this
> interact with DeepSeek-V3 / V4-class routing strategies that have been
> the focus of the 2025-2026 inference-serving literature? What's the
> current state of the art across vLLM, SGLang, TensorRT-LLM, and the
> recent llm-d / LMCache ecosystem, and which approach should a new
> contributor prioritize?

## Assumed interpretation

Akash is a vLLM contributor with ML-systems focus (CERN GSoC background,
IIT-P). The literal prompt is a four-clause research question:
1. *Structural*: how vLLM routes experts when `num_experts > tp_size`
2. *Comparative*: how that interacts with DeepSeek-V3/V4 routing (top-k
   gating, shared experts, auxiliary-loss-free routing, and DeepSeek's
   EP-parallel bag of tricks — DeepEP, grouped-GEMM kernels, MTP, etc.)
3. *Competitive*: head-to-head on vLLM, SGLang, TRT-LLM, and the newer
   llm-d / LMCache ecosystem
4. *Actionable*: "which approach should a new contributor prioritize" —
   Akash is trying to decide where to put his engineering time.

Underlying decision Akash is probably trying to make: **"what's the
highest-leverage vLLM MoE routing PR I could file this quarter, given
that 2025-2026 literature has largely converged on a common playbook
and vLLM's current position relative to SGLang / TRT-LLM is somewhere
between 'leader' and 'catching up'?"**

Not explicitly asked but within scope:
- Memory footprint implications of `num_experts > tp_size` (i.e., each
  rank holding multiple experts + the all-to-all traffic pattern)
- The `EP vs TP vs DP` design-space axis, not just EP-alone
- Failure modes at the boundary where EP-degree changes relative to
  expert count (a.k.a. "irregular expert placement")
- Whether vLLM's upstream MoE kernels are the bottleneck vs routing
  strategy vs all-to-all overhead
- llm-d and LMCache's role — these are the new disaggregated / KV-cache
  systems — do they even touch MoE routing, or is MoE orthogonal?

## Sub-questions (numbered, answered in SYNTHESIS.md)

1. **What is "MoE expert-parallel routing" precisely in 2026 vocabulary**,
   and what does it mean when `num_experts > tp_size` specifically?
   (Definitional — linguist + librarian + historian)

2. **How does vLLM currently implement EP routing** (which files, which
   kernels, which dispatch primitives)? (Cartographer + tracer on GitHub)

3. **What were the key design inflection points in vLLM's MoE code**
   during the 2025 DeepSeek-V3 adoption wave? (Archaeologist / github-miner
   via `gh api` — PRs, issues, release notes)

4. **How does DeepSeek-V3/V4 routing differ** from legacy Switch/Mixtral
   routing, and why did the whole ecosystem re-tool around it in 2025?
   (Historian — the DeepSeek-V3 paper + the DeepSeekMoE v2 paper + the
   2025 papers that built on them)

5. **Same question #2 for SGLang, TensorRT-LLM, llm-d, LMCache**. Where
   does each of them stand on EP routing for `num_experts > tp_size`?
   (Librarian + github-miner)

6. **Benchmark landscape**: what are people publishing as "vLLM vs
   SGLang vs TRT-LLM on DeepSeek-V3" in 2025-2026? How trustworthy are
   those benchmarks? (Web-miner + adversary — THIS is where corpus attacks
   matter most, LinkedIn / Medium benchmark SEO is a real thing)

7. **Back-of-envelope scaling**: for a DeepSeek-V3-class model (671B
   total, 37B active, 256 routed experts + 1 shared), what's the
   all-to-all traffic cost per token at EP=8, 16, 32? Is that a real
   bottleneck or a handwave? (Empiricist)

8. **Contribution leverage**: where are the open PRs / tracked issues
   in vLLM's MoE code in 2026-Q1, and which have the clearest path to
   merge for a new contributor? (Github-miner on vllm-project/vllm)

9. **What are the recurring criticisms and praises** of each framework's
   MoE story in 2026? What's the sentiment drift from mid-2025 to now?
   (Historian + web-miner + linguist)

10. **Failure modes**: where does `num_experts > tp_size` go wrong in
    practice? Load imbalance? All-to-all stragglers? (Skeptic + empiricist)

## Acceptance criteria

For the SYNTHESIS.md to pass the evaluator:
- Every sub-question 1-10 must have an explicit answer section
- ≥ 5 authoritative primary sources cited (papers or official repos),
  not a sea of Medium reposts
- At least one quantitative back-of-envelope calculation from empiricist
- Head-to-head comparison table of vLLM / SGLang / TRT-LLM / llm-d on
  ≥ 4 dimensions
- At least one "here's the PR you should file" concrete recommendation
- Corpus audit from adversary must be "healthy" or "mixed" — not "compromised"
- At least one contradiction must be surfaced and arbitrated by the
  moderator (this is a stress-test pilot — if there's zero contradiction,
  the team probably echo-chambered)

## Known constraints

- This invocation's cwd is `/home/akash/PROJECTS/claude`, which does NOT
  have a vLLM checkout. Cartographer lens must operate on GitHub via
  `gh api` rather than local Grep/Read.
- All specialist personas are executed by the lead (this thread); they
  are behavioral contracts, not separate processes. Per MEMORY.md
  "Subagents cannot spawn subagents".
- Session date: 2026-04-12. Evidence retrieved from docs/papers/posts
  up to this date.
- Full v2 gate chain must run including evaluator + retrospector. This
  is a pilot, not a production session — the goal is to *exercise* every
  gate, not to minimize gate invocations.

## Definition of done

SYNTHESIS.md passes the evaluator's 5-dim rubric, retrospector writes
3-7 durable lessons to MEMORY.md, scribe updates INDEX.md. Final answer
is returned to the executor in ≤200 words.
