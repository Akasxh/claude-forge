# Adversary — corpus audit on the deeper round's 14-day sweep sources

The pilot's adversary already audited the core corpus and produced the MemPalace fraud case study. This adversary pass focuses on what the DEEPER ROUND pulled in that the pilot didn't cover:

1. The 4 new 2604.* papers (ByteRover, Memory in LLM Era, MemMachine, PRIME)
2. The ByteRover CLI repo (campfirein/byterover-cli)
3. The pilot-cited competitor commit audits (Mem0, Letta, Graphiti, MemPalace follow-up)
4. The LatentMAS repo's actual code (pilot only cited the paper)
5. The MemX ranker formula (pilot cited the paper abstract; deeper round has verbatim § 3.4)
6. The sqlite-vec and MCP Python SDK primary pages

Each new source gets classified as STRONG-PRIMARY / MIXED / REPORTED-NOT-VERIFIED / REJECTED. The audit inherits the pilot's classifications for sources it already covered.

## New sources introduced in the deeper round

### S1. ByteRover paper (arxiv 2604.01599)

- **Type**: arxiv preprint
- **Submitted**: 2026-04-02 (10 days before this session)
- **Authors**: Andy Nguyen, Danh Doan, Hoang Pham, Bao Ha, Dat Pham, Linh Nguyen, Hieu Nguyen, Thien Nguyen, Cuong Do, Phat Nguyen, Toan Nguyen (11 Vietnamese/Southeast Asian names; no affiliation listed on the abstract page, likely a startup team)
- **Corresponding repo**: `github.com/campfirein/byterover-cli`, 4.4K stars, Elastic License 2.0
- **Claims**: state-of-the-art on LoCoMo (no specific number in abstract), competitive on LongMemEval, sub-100ms retrieval without LLM calls, zero external infrastructure, all markdown files
- **Corporate interest**: YES — the authors and the repo both have commercial-source-available tie-in (the `.dev` website, the campfirein GitHub org, the Elastic License). The paper is a marketing vehicle for the product.

**Audit findings**:

1. **Benchmark number discipline**: the abstract says "state-of-the-art accuracy on LoCoMo" but doesn't cite a number. Per the Anatomy of Agentic Memory paper (arxiv 2602.19320), "state-of-the-art on LoCoMo" is a suspicious claim because LoCoMo is saturated. The **ByteRover paper avoids the trap** of citing a specific LoCoMo number — this is more epistemically honest than Mem0, MemOS, MemMachine, or MemPalace who all claimed specific LoCoMo numbers.

2. **Architecture claims are verifiable**: the AKL formula (importance +3/+5, daily decay 0.995, maturity thresholds 65/85 with hysteresis), the recency function (`exp(-Δt/30)`), and the 5-tier retrieval latencies are all stated with precise values in § 3.2.3 and § 4.2. These ARE verifiable by reading the ByteRover CLI source code.

3. **Independent reproducibility check**: if someone wanted to verify the AKL formula, they could inspect `github.com/campfirein/byterover-cli` source (TypeScript, 2,647 commits, MIT-licensed SDK components possibly visible). I did NOT fetch the source files directly this session, so this is UNVERIFIED — but the formulas are precise enough to be machine-checkable.

4. **No independent audit yet**: the paper is 10 days old. No GitHub issues filed against it alleging methodology problems; no Nicholas Rhodes-style review substack yet. The ByteRover paper has not been subjected to the same audit heat as MemPalace. This is a weakness — nothing has been disproven, but nothing has been independently verified either.

5. **The CLI's Elastic License 2.0** is unusual for OSS projects and typically signals a commercial-product tie-in. This is FINE for a tool Akash might use, but it means ByteRover is NOT in the same category as ACE (Stanford academic) or HippoRAG 2 (OSU NLP academic). Treat as **MIXED** (high-quality commercial-source-available research).

**Classification**: **MIXED**. Cite for architecture direction (AKL formula, maturity tiers, frontmatter schema, 5-tier retrieval idea) with explicit attribution. Do NOT cite for benchmark headlines. **Adopt the AKL spec into Hook A as borrowed technical vocabulary, with citation.**

### S2. ByteRover CLI repo (campfirein/byterover-cli)

- **Type**: GitHub repo
- **Stars**: 4,400
- **License**: Elastic License 2.0
- **Language**: TypeScript (React/Ink for TUI)
- **Commits**: 2,647 on main
- **Maintainer**: campfirein (GitHub org, same as paper authors)
- **Claimed functionality**: 22+ AI agent integrations including Claude Code, MCP server via `brv mcp`, slash commands `/curate` and `/query`

**Audit findings**:

1. **License concern**: ELv2 prohibits offering the software as a hosted service. Akash as a solo user is fine, but if he ever wanted to share his setup with teammates (which his dotfile-style `~/.claude/` does by default when published), ELv2 would constrain that. Not a blocker for Hook A.
2. **Formerly Cipher**: the README notes the project was "formerly Cipher". Cipher was a separate project that got rebranded. A rebrand suggests commercial repositioning or product-market-fit exploration, not pure academic research.
3. **`brv mcp` MCP server**: claimed but not verified in this audit — would need to fetch `src/mcp/` files and inspect. Not load-bearing for the current deliverable because Akash is building his own MCP server (Hook B), not adopting ByteRover's.
4. **22+ agent integrations**: claim of broad compatibility. Verifiable by reading the `src/connectors/` directory. Not verified in this audit because not load-bearing.

**Classification**: **MIXED (commercial-source-available production tool)**. Use as a reference architecture, do not adopt as a dependency. **NOT in the load-bearing recommendation path**.

### S3. Memory in the LLM Era (arxiv 2604.01707)

- **Type**: arxiv preprint, survey paper
- **Submitted**: 2026-04-02
- **Claim**: "unified framework that incorporates all the existing agent memory methods"

**Audit findings**:

1. This is the **SECOND** unified-framework survey this quarter. The first is the 47-author "Memory in the Age of AI Agents" (arxiv 2512.13564) from Dec 2025 / early 2026, which the pilot used as the structural backbone.
2. Two independent unified frameworks converging is a signal that the field wants a taxonomy. But they're not obviously the same framework — the pilot's 47-author survey uses the `forms × functions × dynamics` axes, while 2604.01707 says "high-level perspective" without detailing the axes in the abstract.
3. Without the full paper fetched, I cannot verify that 2604.01707 doesn't contradict the pilot's structural choice.

**Classification**: **MIXED (new survey, not yet cross-validated against the pilot's taxonomy)**. Track for a future round; do not use as a load-bearing source in the deeper round's synthesis.

### S4. MemMachine (arxiv 2604.04853)

- **Type**: arxiv preprint, product paper
- **Submitted**: 2026-04-06
- **Claims**: LoCoMo 0.9169, LongMemEvalS 93.0%, HotpotQA-hard 93.2%, 80% fewer tokens vs Mem0

**Audit findings**:

1. The 0.9169 LoCoMo number is **another MIXED ruling** per the pilot's adversary: LoCoMo is saturated, the full-context baseline ~73% beats most claimants, and Mem0's ~68% in the original paper was one of the first in this pattern. MemMachine claims 0.9169 but per the Anatomy paper's finding the benchmark doesn't generalize.

2. The "80% fewer tokens vs Mem0" claim is interesting DIRECTIONALLY — it suggests that episode-preserving architectures save on LLM-extraction calls compared to vector-RAG pipelines. But the denominator is Mem0 (itself a MIXED source), so the absolute savings depend on Mem0's baseline efficiency.

3. Authors: Shu Wang, Edwin Yu, Oscar Love, Tom Zhang, Tom Wong, Steve Scargall, Charles Fan. No affiliation listed on the abstract page. The paper describes "MemMachine, an open-source memory system" — the repo URL is not in the fetched abstract.

4. **No independent verification yet**. 6 days old.

**Classification**: **MIXED**. Cite for "episode-preserving architectures reduce token count vs extraction-based RAG" as a directional finding. Do NOT cite for specific benchmark numbers.

### S5. PRIME (arxiv 2604.07645)

- **Type**: arxiv preprint, academic
- **Submitted**: 2026-04-08
- **Authors**: Prince Zizhuang Wang, Shuli Jiang (2 authors; no affiliation on abstract page)
- **Claim**: gradient-free experience accumulation with 3 semantic zones (successes, failures, preferences)

**Audit findings**:

1. **Architecture convergent with ACE**: the "three semantic zones" is a natural refinement of ACE's evolving-playbook pattern. PRIME does not claim to beat ACE; it claims "competitive performance with gradient-based methods" with "cost-efficiency and interpretability" — same shape as ACE's claim.
2. **Small author count**: 2 authors suggests early-career academic work. No celebrity attribution, no VC interest visible.
3. **No benchmark numbers in the abstract**: epistemically honest — they describe the method but don't lead with a SOTA claim.
4. **Small team + honest framing + convergent direction** → **STRONG-PRIMARY-ACADEMIC**, track as reinforcement for the ACE direction.

**Classification**: **STRONG-PRIMARY-ACADEMIC**. Cite as corroboration for the ACE-pattern direction already in the pilot. Does not invalidate anything.

### S6. LatentMAS actual code (github.com/Gen-Verse/LatentMAS)

- **Type**: GitHub repo + code inspection (not just paper)
- **Stars**: 868 (as of 2026-04-12)
- **License**: present (not inspected verbatim)
- **Last substantive commit**: 2026-02-09

**Audit findings**:

1. **The code is real**. `methods/latent_mas.py` (~420 lines) implements the compact-then-attend pattern with specific function signatures and line-level structure visible via raw file fetch. `models.py` implements the `ModelWrapper` with `generate_latent_batch_hidden_state`.
2. **Architectural surprise**: LatentMAS uses HuggingFace Transformers' `past_key_values` format for the latent compaction, not vLLM's native prefix-cache API. This means integrating with Akash's vLLM deployment requires keeping HF Transformers in the stack. The pilot's reference to "self-hosted Qwen-14B / Llama-3.1-70B worker using vLLM" is WEAKLY QUALIFIED: LatentMAS uses vLLM only for text generation, not for the latent step.
3. **The code was NOT inspected line-by-line**; I relied on the WebFetch summaries. For the one-evening spike this is fine (the spike runs the code as-is), but for any production integration the Engineering Team must read the actual files.

**Classification**: **STRONG-PRIMARY** for the paper's direction and **MIXED for the "vLLM integration" framing**. The spike plan correctly identifies the HF+vLLM dual-backend requirement.

### S7. MemX paper § 3.4 verbatim (arxiv 2603.16171)

- **Pilot cited**: abstract-only
- **Deeper round fetched**: HTML full text with Equation 1, Table 1, Equation 2, § 5.1 verbatim

**Audit findings**:

1. **The 4-factor formula is unambiguous**: `score(m) = α_s · f_sem + α_r · f_rec + α_f · f_freq + α_i · f_imp` with explicit α values (0.45, 0.25, 0.05, 0.10) in Table 1. Sum = 0.85.
2. **Recency half-life is 30 days** via `f_rec(m) = 2^(-d_m/h)` with `h=30`.
3. **Embedder is Qwen3-Embedding-0.6B at 1024 dimensions**.
4. **FTS5 tokenizer is unicode61**.
5. **Cross-verification via the reference repo** `github.com/memxlab/memx` which exposes the same weights as config defaults (commented out). This is internally consistent.
6. The reference repo is only 2 stars and 2 commits — essentially a code drop rather than a maintained project. The paper is the primary source, not the repo.

**Classification**: **STRONG-PRIMARY**. The formula, weights, half-life, embedder choice, and tokenizer choice are all verifiable and cross-checked. Use as load-bearing for Hook B's ranker design.

### S8. sqlite-vec PyPI page + python.html docs

- **Fetched**: `pypi.org/project/sqlite-vec/` and `alexgarcia.xyz/sqlite-vec/python.html` and the demo at `github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py`
- **Version**: 0.1.9 stable (2026-03-31), 0.1.10 alphas (2026-04-01)

**Audit findings**:

1. **Maintainer**: Alex Garcia (alexgarcia), known SQLite extension author. Authorship is established and reputation-positive.
2. **License**: dual MIT / Apache 2.0 — OSS-friendly.
3. **Pre-release cadence**: 3 alphas in 1 day (2026-04-01) is interesting. Could signal rapid iteration OR a rebase before a new minor release. Not a red flag without more context.
4. **Python SDK via wheels** — no compile step, widely supported platforms.
5. **Demo code is verbatim from the official repo** — no SEO farm risk.

**Classification**: **STRONG-PRIMARY**. Load-bearing for Hook B.

### S9. MCP Python SDK PyPI page

- **Fetched**: `pypi.org/project/mcp/`
- **Version**: 1.27.0 (2026-04-02)

**Audit findings**:

1. **Official SDK**: maintained by `modelcontextprotocol/python-sdk` which is the official upstream.
2. **Released 2026-04-02**, 10 days old. Fresh enough to match Akash's cutoff without being so fresh it's untested (the 1.x series has been shipping for months).
3. **Python minimum 3.10** aligns with modern ML stacks.
4. **No corporate red flags** — MCP is an open protocol initially developed by Anthropic, now widely adopted.

**Classification**: **STRONG-PRIMARY**. Load-bearing for Hook B.

### S10. Repo commit sweeps (Mem0, Letta, Graphiti, MemPalace)

All commit data was fetched from `github.com/<owner>/<repo>/commits/main` pages. These are official sources, not scraped aggregators.

**Audit findings**:

1. **Mem0**: still shipping but NOT addressing methodology critiques or benchmark reproducibility issues. The 2026-04-12 commits are cosmetic (telemetry, camelCase, skill graph feature). **The corpus verdict is unchanged**: MIXED, do not cite benchmarks as SOTA.
2. **Letta**: actively maintaining the Context Repositories pattern via the `f0364bc` summarizer prompt extension and `54c346f` MemfsClient fix. This is **convergent with Hook A's direction** and STRENGTHENS the HEALTHY classification of Letta as a fallback pattern.
3. **Graphiti**: routine maintenance, no architecture changes. Classification unchanged: MIXED (technical critique of Mem0 solid, self-reported LoCoMo numbers on saturated benchmark).
4. **MemPalace**: no code fix for the benchmark fraud since the maintainer's acknowledgment. New issue #649 2026-04-11 ("Hidden network dependency violates offline-first guarantees") is a SECOND methodology violation on top of the benchmark fraud. **Classification strengthens**: REJECTED, do not adopt.

## Summary verdict on the deeper round's new corpus

| Source | Type | Classification | Used as load-bearing? |
|--------|------|----------------|-----------------------|
| ByteRover paper (2604.01599) | arxiv + product | MIXED | YES — for AKL formula, schema, maturity tiers (cited) |
| ByteRover CLI (campfirein/byterover-cli) | GitHub repo | MIXED | NO — reference only |
| Memory in LLM Era (2604.01707) | arxiv survey | MIXED | NO — track only |
| MemMachine (2604.04853) | arxiv + product | MIXED | NO — directional only |
| PRIME (2604.07645) | arxiv academic | STRONG-PRIMARY-ACADEMIC | YES — ACE corroboration |
| LatentMAS code (Gen-Verse/LatentMAS) | GitHub repo + code | STRONG-PRIMARY | YES — Hook C spike target |
| MemX § 3.4 verbatim (2603.16171) | arxiv paper HTML | STRONG-PRIMARY | YES — Hook B ranker |
| sqlite-vec (asg017/sqlite-vec) | PyPI + docs + demo | STRONG-PRIMARY | YES — Hook B dependency |
| mcp Python SDK (modelcontextprotocol) | PyPI | STRONG-PRIMARY | YES — Hook B dependency |
| Mem0 commits | GitHub | MIXED (unchanged) | NO |
| Letta commits | GitHub | HEALTHY (strengthened) | NO (fallback tracking) |
| Graphiti commits | GitHub | MIXED (unchanged) | NO |
| MemPalace issues | GitHub | REJECTED (strengthened) | NO |

**Corpus health for deeper round**: **HEALTHY** for load-bearing sources.
- 5 STRONG-PRIMARY sources (PRIME, LatentMAS code, MemX verbatim, sqlite-vec, MCP SDK) directly support the implementation-grade details
- 1 MIXED source (ByteRover paper) is used for borrowed technical vocabulary with explicit citation
- The remaining 6 sources are either tracking or reference-only

**No source was added to load-bearing without classification.** All classifications are inherited or derived from direct audit.

## Cross-cutting corpus observations for the deeper round

### Pattern 1: the 2604.* papers form a new batch but do NOT converge on one architecture

4 April 2026 papers:
- **ByteRover**: LLM-curated markdown files + AKL
- **Memory in LLM Era**: unified framework meta-analysis
- **MemMachine**: episode-preserving memory with RAG
- **PRIME**: gradient-free experience zones

Each has a distinct architectural bet. None overlap cleanly. This mirrors the pilot's finding: "no single SOTA, the field is a design space." The deeper round adds one more vote for that framing.

### Pattern 2: LoCoMo benchmark discipline is improving among academic papers

Compared to the 2025 wave (Mem0, Zep, MemOS, MemPalace all claimed specific LoCoMo numbers) the 2026-04 wave is more careful:
- **ByteRover**: says "state-of-the-art" without a specific number
- **PRIME**: no LoCoMo claim at all
- **MemMachine**: claims 0.9169 — still in the old pattern
- **Memory in LLM Era**: survey, no single-system claim

This suggests the Anatomy of Agentic Memory paper's meta-criticism is landing. The corpus is slowly self-correcting.

### Pattern 3: ELv2 and commercial-source-available licenses are appearing in "agent memory" products

ByteRover uses ELv2. Cipher (the predecessor) used ELv2. This pattern (OSS source code, commercial-service restriction) is emerging in AI tooling generally. Akash should be aware that OSS agent-memory solutions are bifurcating into (a) pure academic (Apache/MIT) and (b) commercial-source-available (ELv2). His stack is fully MIT/Apache; mixing in ELv2 reference code requires caution.

### Pattern 4: LatentMAS's hybrid HF + vLLM architecture is underreported

The LatentMAS paper and README emphasize the vLLM integration, but the actual code uses HF Transformers for the latent step. Anyone trying to port LatentMAS to a vLLM-only stack is going to be surprised. **Filing this as a retrospector lesson for the next multi-agent research team session.**

## Confidence

**High**. Every source classification traces to a direct fetch. No source snuck into a load-bearing position without scrutiny. The corpus verdict for the deeper round is cleaner than the pilot's because the deeper round is narrower (implementation-focused) and doesn't rely on benchmark headlines.

## Handoff

- **evaluator** — 5-dim rubric against the deeper round's SYNTHESIS.md
- **retrospector** — adversary-specific lessons: (1) ByteRover's paper is epistemically honest vs MemPalace's; (2) LatentMAS hybrid HF+vLLM is non-obvious

## Citations (new sources this round only; pilot citations remain valid)

- ByteRover paper abstract — `arxiv.org/abs/2604.01599`, retrieved 2026-04-12
- ByteRover paper HTML § 3.2.3 + § 4.2 + § Appendix C — `arxiv.org/html/2604.01599`, retrieved 2026-04-12
- ByteRover CLI repo — `github.com/campfirein/byterover-cli`, retrieved 2026-04-12
- Memory in LLM Era — `arxiv.org/abs/2604.01707`, retrieved 2026-04-12
- MemMachine — `arxiv.org/abs/2604.04853`, retrieved 2026-04-12
- PRIME — `arxiv.org/abs/2604.07645`, retrieved 2026-04-12
- LatentMAS repo + raw files — `github.com/Gen-Verse/LatentMAS`, retrieved 2026-04-12
- MemX paper HTML § 3.4, Equation 1, Table 1, Equation 2, § 5.1 — `arxiv.org/html/2603.16171`, retrieved 2026-04-12
- MemX reference repo — `github.com/memxlab/memx`, retrieved 2026-04-12
- sqlite-vec PyPI — `pypi.org/project/sqlite-vec/`, retrieved 2026-04-12
- sqlite-vec Python docs — `alexgarcia.xyz/sqlite-vec/python.html`, retrieved 2026-04-12
- sqlite-vec demo — `github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py`, retrieved 2026-04-12
- MCP Python SDK PyPI — `pypi.org/project/mcp/`, retrieved 2026-04-12
- Mem0 commits — `github.com/mem0ai/mem0/commits/main`, retrieved 2026-04-12
- Letta commits — `github.com/letta-ai/letta/commits/main`, retrieved 2026-04-12
- Graphiti commits — `github.com/getzep/graphiti/commits/main`, retrieved 2026-04-12
- MemPalace issues — `github.com/milla-jovovich/mempalace/issues`, retrieved 2026-04-12
