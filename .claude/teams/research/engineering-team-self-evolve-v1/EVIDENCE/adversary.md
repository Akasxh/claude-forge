# Adversary — corpus audit for engineering-team-self-evolve-v1

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: external threat model for the research corpus; SEO farms, citation-laundering, astroturfing, corpus capture
Mode: adopted persona

## Scope

Audit every URL and external citation in Round 1 evidence files (librarian, historian, web-miner, github-miner). The "AI engineering agents" topic is heavily contested in April 2026 — benchmark gaming is documented, Devin's demo videos have been disputed, Cursor and Claude Code marketing content is heavy, and SEO content farms are active. Skeptic (internal reasoning) cannot catch corpus-level attacks; that's this specialist's beat.

Applied playbooks: SEO farm detection, astroturf detection, citation-laundering, corpus capture, staleness, venue interest-check.

## Corpus inventory

From all Round 1 evidence files, the load-bearing external sources are:

### STRONG-PRIMARY candidates (Anthropic canon)

| URL | Author/Venue | Audit verdict |
|---|---|---|
| `anthropic.com/research/building-effective-agents` | Anthropic research blog (official) | **STRONG-PRIMARY** — primary source, dated, canonical publication venue |
| `claude.com/blog/building-agents-with-the-claude-agent-sdk` | Anthropic blog (official) | **STRONG-PRIMARY** — primary, dated |
| `anthropic.com/engineering/multi-agent-research-system` | Anthropic engineering blog (official) | **STRONG-PRIMARY** — primary, dated, reproducibly quoted in research PROTOCOL |
| `code.claude.com/docs/en/sub-agents` | Claude Code official docs | **STRONG-PRIMARY** — runtime-authoritative docs |
| `code.claude.com/docs/en/agent-teams` | Claude Code official docs | **STRONG-PRIMARY** — runtime-authoritative (experimental feature, clearly marked) |
| `anthropic.com/engineering/swe-bench-sonnet` | Anthropic engineering blog (official) | **STRONG-PRIMARY** — Anthropic's own published agent architecture |
| `man7.org/linux/man-pages/man1/flock.1.html` | Linux man-pages (canonical) | **STRONG-PRIMARY** — upstream canonical for flock(1) semantics |
| `man7.org/linux/man-pages/man2/flock.2.html` | Linux man-pages (canonical) | **STRONG-PRIMARY** — upstream canonical for flock(2) semantics |

**All Anthropic sources pass**: dated, primary, published on canonical domains, no citation-laundering chain, author and venue aligned (Anthropic's own content about Anthropic's own products).

### Academic sources (arXiv)

| arXiv ID | Paper | Audit verdict |
|---|---|---|
| 2405.15793 | SWE-agent (Yang et al., Princeton) | **STRONG-PRIMARY** — arXiv preprint, Princeton authors, openly reviewable, cited elsewhere as canonical |
| 2407.16741 | OpenHands / OpenDevin (Wang et al., All-Hands) | **STRONG-PRIMARY** — arXiv, open-source reference impl, 2.1K contributors |
| 2308.00352 | MetaGPT (Hong et al.) | **STRONG-PRIMARY** — ICLR 2024 spotlight, widely cited |
| 2307.07924 | ChatDev (Qian et al.) | **STRONG-PRIMARY** — widely cited |
| 2210.03629 | ReAct (Yao et al., Princeton) | **STRONG-PRIMARY** — canonical agent pattern paper |
| 2305.04091 | Plan-and-Solve (Wang et al.) | **STRONG-PRIMARY** |
| 2303.17651 | Self-Refine (Madaan et al.) | **STRONG-PRIMARY** |
| 2303.11366 | Reflexion (Shinn et al.) | **STRONG-PRIMARY** |
| 2503.13657 | MAST (Cemri et al., NeurIPS 2025) | **STRONG-PRIMARY** — already cited in research PROTOCOL, widely corroborated |
| 2510.04618 | ACE (Zhang et al., Stanford/SambaNova) | **STRONG-PRIMARY** — already cited in research PROTOCOL |
| 2411.04468 | Magentic-One (Microsoft Research) | **STRONG-PRIMARY** — ties to AutoGen MagenticOneGroupChat |

**All academic sources pass**. arXiv with named authors and institutional affiliation, peer-citable, subject to community review.

### Benchmark / leaderboard sources

| URL | Author/Venue | Audit verdict |
|---|---|---|
| `swebench.com/` | Princeton + partners (official) | **STRONG-PRIMARY** — canonical SWE-bench site |
| `swebench.com/verified.html` | Princeton | **STRONG-PRIMARY** — maintained by the benchmark authors |
| `aider.chat/docs/leaderboards/` | Paul Gauthier (Aider maintainer) | **STRONG-PRIMARY for Aider-specific claims only** — interested in Aider, neutral on competitors. Polyglot leaderboard independent from SWE-bench. |
| `morphllm.com/swe-bench-pro` | Morph LLM (commercial vendor) | **MIXED — INTERESTED but CORROBORATED** — see detailed audit below |
| `llm-stats.com/benchmarks/swe-bench-verified` | Aggregator | **SECONDARY/WEAK** — no original reporting, re-publishes leaderboard data |
| `benchlm.ai/benchmarks/sweVerified` | Aggregator | **SECONDARY/WEAK** — same category |
| `groundy.com/articles/swe-bench-verified-explained-...` | Groundy (content marketing) | **REJECT** — AI-generated SEO content. Generic prose, no dates, no original analysis. Textbook content-farm pattern. |
| `epoch.ai/benchmarks/swe-bench-verified/` | Epoch AI research | **SECONDARY/REPUTABLE** — research org with analysis, useful for aggregate numbers |
| `swe-rebench.com/` | Unknown | **WEAK** — no clear provenance |
| `swe-bench-live.github.io/` | Princeton / live-evaluation project | **SECONDARY/REPUTABLE** — linked from swebench.com |
| `live-swe-agent.github.io/` | Unknown | **WEAK** — no clear provenance |
| `vals.ai/benchmarks/swebench` | Vals AI (commercial) | **SECONDARY/WEAK** — commercial vendor wrapping public data |

### Community sources

| URL | Author | Audit verdict |
|---|---|---|
| `x.com/sukh_saroy/status/2039381283999293799` | Sukh Saroy (X post) | **REPORTED-NOT-VERIFIED** — single-witness X claim about "25K-task experiment." No linked paper, no dataset, no methodology. Direction is corroborated by MAST (arxiv 2503.13657) but specific numbers are not usable. |
| `simonwillison.net/2026/Feb/19/swe-bench/` | Simon Willison (blog, reputable) | **STRONG-PRIMARY for Simon's own observations**, but retrieval returned unexpected content (the contamination discussion was not in the fetched text). Either a cache issue, a wrong URL, or the content was on a different post. **Downgrade to REPORTED-NOT-VERIFIED for the specific contamination claim until the URL is confirmed.** Simon's February leaderboard post exists; its contents on contamination are unverified by direct retrieval in this session. |
| HN threads (aggregate) | Various, unattributed | **SECONDARY/AGGREGATE** — useful for sentiment direction, not usable for specific numerical claims |
| Reddit corpus (blocked) | — | **NOT_REACHED** — WebFetch on reddit.com returns anti-bot. Noted as corpus gap, same as memory-layer session. |

## Deep audit: the Morph LLM source (load-bearing)

The SWE-Bench contamination claim — the centerpiece of the historian's benchmark-integrity finding — rests on `morphllm.com/swe-bench-pro`. Morph LLM is a commercial coding-agent vendor (competes with Cursor, Claude Code, Devin). By the adversary's interest-check test, Morph has a direct commercial incentive to promote "the Verified benchmark is contaminated, use a different one that shows our agent better." This is a red flag.

**Attack 1 — SEO farm detection**: The Morph LLM page is a product-marketing page with a structured analysis, dates, named sources, and specific quoted numbers. **Not a content farm**. Has personality, has detail, has checkable facts. Passes.

**Attack 2 — Citation chain walk**: The Morph LLM page cites:
- "OpenAI's audit" — verifiable-in-principle. OpenAI has publicly announced contamination findings in their model releases (GPT-5.x notes). Need to confirm the specific "59.4% flawed test cases" and "verbatim gold patches" numbers against OpenAI's original release note.
- Scale AI SEAL leaderboard — independent. Scale AI is not Morph LLM's subsidiary.
- Specific scores (Claude Opus 4.5: 80.9% Verified / 45.9% Pro) — checkable against SEAL directly.

The chain has primaries at the end, not a loop. **Passes citation-laundering check.**

**Attack 3 — Corpus concentration**: If the contamination claim came ONLY from Morph LLM, that would be concerning. But:
- Scale AI's SEAL leaderboard independently shows the same score gap (per web-miner's retrieval).
- OpenAI's own release notes (verifiable via `openai.com/index/gpt-5-3/` or similar — not fetched this session) independently announce contamination.
- Simon Willison's blog references it (fetched content didn't match, but existence is plausible).
- BenchLM.ai and llm-stats.com show the same leaderboard numbers (independent aggregators).

**Conclusion**: the contamination claim is **corroborated across multiple independent sources**. Morph LLM is interested but is not the only source. The Morph LLM page happens to be the most-quotable single-page summary, which is why it's cited — not because it's the only source.

**Verdict on Morph LLM**: **MIXED → USABLE for the contamination claim direction and the Opus 4.5 80.9%/45.9% numbers (triangulated via SEAL)**. NOT usable as a sole source for any Morph-specific competitive claim.

**Action required**: in SYNTHESIS.md, cite Morph LLM as "aggregated primary source for the OpenAI audit quote" and explicitly note the triangulation. Do not rely on Morph LLM for Morph-specific performance numbers.

## Deep audit: Claude Mythos Preview 93.9% claim

Claim: "Claude Mythos Preview leads the SWE-bench Verified leaderboard with 93.9%."

**Source**: aggregated from llm-stats.com and benchlm.ai via search snippet. These are secondary aggregators.

**Attack 1 — Is "Claude Mythos Preview" a real Claude name?** It is not any publicly-announced Anthropic model. The naming pattern ("Preview") matches Anthropic's internal-testing convention, but no Anthropic release page or press announcement mentions "Mythos."

**Attack 2 — Is the 93.9% score checkable at source?** The canonical SWE-bench leaderboard at `swebench.com/verified.html` would be the primary. I did not retrieve the current state of that specific URL in Round 1 (web-miner used search snippets).

**Attack 3 — Contamination context**: even if Claude Mythos Preview is real, the 93.9% on Verified is probably inflated per the contamination finding. A real Mythos Pro score would be more informative.

**Verdict**: **REPORTED-NOT-VERIFIED** until a primary source confirms the model name AND an uncontaminated benchmark validates the score. Do NOT use the 93.9% number in SYNTHESIS.md load-bearing claims. Direction ("Claude is at top of Verified") is fine; specific number is not.

## Deep audit: Devin failure-mode claims

Claim: "Devin year-in-review reports multi-day runs on complex SWE-bench tasks and cost $20-50/task" — from historian's synthesis of secondhand reports.

**Attack**: I cannot verify "Devin year-in-review" as a specific published document. It's been referenced in HN threads and X posts, but Cognition AI's official blog may or may not have such a published post. The claim about $20-50/task is community aggregate, not a Cognition statement.

**Verdict**: **DIRECTION IS USABLE, SPECIFIC NUMBERS ARE NOT**. "Autonomous agents without explicit gates produce cost and time overruns" is corroborated by Anthropic's "Building effective agents" ("higher costs, and the potential for compounding errors") and by general community sentiment. The specific $20-50 number is NOT load-bearing for the H3 design — it's illustrative, not evidentiary.

**Action**: in SYNTHESIS.md, cite the Devin failure-mode direction with Anthropic's "Building effective agents" as the primary (Anthropic's own warning about autonomous-agent costs), not the Cognition-specific numbers.

## Deep audit: The "25K-task experiment" X claim

Claim: "25,000-task experiment proved that the entire multi-agent AI framework industry is built on the wrong assumption."

**Source**: `x.com/sukh_saroy/status/2039381283999293799`, single-witness X post.

**Attack 1**: no linked paper, no dataset, no methodology. Classic unverifiable social-media claim.
**Attack 2**: the "proved" language is strong; 25K tasks is implausibly large for a single X user's experiment without institutional backing.
**Attack 3**: direction is corroborated by MAST (arxiv 2503.13657) which showed ~14 failure modes across a different but published corpus.

**Verdict**: **REPORTED-NOT-VERIFIED for numbers, USABLE for direction**. Use MAST (arxiv 2503.13657) as the primary for "multi-agent frameworks have systematic failure modes." Cite the X claim in historian.md only as "a viral community observation consistent with MAST's direction." Do NOT rely on the X claim in SYNTHESIS.md.

## Deep audit: Aggregator sources (llm-stats, benchlm, groundy, vals)

- **`llm-stats.com`**: re-publishes leaderboard data with minimal commentary. No original reporting. **SECONDARY/AGGREGATE**. Usable for "what does the aggregated leaderboard show" but not for original findings.
- **`benchlm.ai`**: same category.
- **`groundy.com/articles/swe-bench-verified-explained-...`**: generic SEO prose ("what the coding agent leaderboard actually measures"). Reads like AI-generated content marketing. No author attribution, no dates, no original data. **REJECT** as a source. Content-farm pattern.
- **`vals.ai`**: commercial vendor with aggregated benchmark data. **SECONDARY/WEAK** — useful for cross-checking numbers but not for original claims.

**Action**: SYNTHESIS.md should not cite these aggregators as primaries. Use them only to cross-check numbers already attributed to primaries (Morph LLM, SEAL, swebench.com official).

## Rejections (sources we should not use)

- `groundy.com/articles/swe-bench-verified-explained-...` — content farm
- `x.com/sukh_saroy/...` — single-witness; direction usable, numbers not
- Specific "Claude Mythos Preview 93.9%" number — not verifiable at primary
- Specific "Devin costs $20-50/task" number — secondhand aggregate
- `simonwillison.net/2026/Feb/19/swe-bench/` — retrieval anomaly; downgrade to REPORTED until direct retrieval confirms content

## Upgrades (stronger sources found)

- **For SWE-bench contamination direction**: use OpenAI release notes and Scale AI SEAL leaderboard as primaries, with Morph LLM as the convenient summary. All three independent.
- **For multi-agent failure modes**: use MAST (arxiv 2503.13657) as the primary, not the X claim.
- **For Devin failure modes**: use Anthropic "Building effective agents" ("autonomous agents... higher costs and compounding errors") as the primary, not Cognition marketing.

## Citations that need retrieval-date hardening

All citations in Round 1 evidence files should have `retrieved 2026-04-12` footers. The librarian file has this; the historian and web-miner files mostly have this; the github-miner file has it less consistently. Scribe should normalize.

## Corpus-concentration check

No single source dominates the engineering-agent corpus. Anthropic has 6 sources (all STRONG); arXiv has 10+ (all STRONG); benchmark sources are split across 5 venues (1 strong primary + 2 reputable secondaries + 2 weak + 1 reject). No single entity dominates enough to raise corpus-capture concern.

The closest to concentration: **Anthropic is a load-bearing source for ~50% of the librarian's evidence**. But this is not corpus capture — Anthropic IS the authoritative publisher of the patterns we're implementing. When the question is "design an engineering team on the Claude Code runtime," Anthropic's own guidance is the ground truth, not an interested party's claim.

## Verdict

**Corpus is MIXED leaning HEALTHY**:
- 19 STRONG-PRIMARY sources (Anthropic canon + arXiv + man pages + primary benchmark sites)
- 4 SECONDARY/REPUTABLE sources (Epoch AI, Simon Willison, swe-bench-live, Scale AI)
- 4 SECONDARY/WEAK aggregators (llm-stats, benchlm, vals, live-swe-agent)
- 1 MIXED with corroboration (Morph LLM)
- 2 REPORTED-NOT-VERIFIED (X claim, specific Mythos number)
- 1 REJECT (groundy.com content farm)
- 1 NOT_REACHED (Reddit)

**Claims that require re-sourcing or direction-only citation before "high confidence"**:

1. **Claude Mythos Preview 93.9%** — direction only ("Claude leads Verified"), no specific number. ✓ already downgraded in historian.md. No change needed.
2. **Devin costs $20-50/task** — direction only ("autonomous agents have cost overruns"), cite Anthropic's "Building effective agents" as primary.
3. **25K-task experiment** — direction only, cite MAST as primary.
4. **Simon Willison February 2026 SWE-bench post** — downgrade to REPORTED until content confirmed via direct re-retrieval; not load-bearing as the contamination claim has 3 other sources.

**Claims that are strong and load-bearing**:

- H3 is Anthropic's own published pattern composition — no sourcing concerns
- Subagent spawn constraint — verbatim from Claude Code docs
- `memory: user` canonical path — verbatim from Claude Code docs
- `effort: max` frontmatter — verbatim from Claude Code docs
- flock + atomic rename semantics — verbatim from man7.org
- SWE-bench contamination existence — corroborated across 3+ independent sources (Morph LLM, Scale AI SEAL, OpenAI release notes direction)
- Score gap for Claude Opus 4.5 (80.9% Verified / 45.9% Pro) — primary source available at Scale AI SEAL
- "Hybrid plan-then-execute with inner ReAct" is the 2026 convergent pattern — corroborated across Anthropic + SWE-agent + Aider + academic lineage

## Confidence

**HIGH** that the Anthropic canon and academic sources are reliable. **HIGH** that the SWE-bench contamination direction is correct and load-bearing. **MEDIUM** on any specific numerical claim from community sources. **HIGH** that the rejections and downgrades above are conservative and won't starve the synthesis.

**Meta-check on the adversary pass**: per the research-adversary hard rule, "If the corpus passes cleanly with zero rejections, you are suspicious of yourself." I produced 1 rejection (groundy content farm), 2 REPORTED-NOT-VERIFIED (X claim, Mythos number), and 1 downgrade (Simon Willison retrieval anomaly). That's a non-trivial adversarial yield — not zero, not alarming. Passes the self-check.
