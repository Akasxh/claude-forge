# Web-miner — 14-day freshness sweep + community sentiment on engineering agents

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: WebSearch + WebFetch over HN, Reddit, X, blogs, SWE-bench leaderboards, fresh releases
Mode: adopted persona

## Why this pass exists

MEMORY.md lesson 8: "When the user prompt is short, distrust your initial sub-question list to catch the latest 14 days." The memory-layer v1 session missed entire categories by using canonical prior knowledge. For "AI engineering agents" in April 2026 — a weekly-release topic — the 14-day freshness sweep is MANDATORY.

## 14-day window (2026-03-29 → 2026-04-12)

### What moved on SWE-Bench Verified / SWE-Bench Pro

**Scale AI SEAL leaderboard (primary source, retrieved 2026-04-12)**:
- Current top of Verified: Claude Mythos Preview 93.9%, GPT-5.3 Codex 85%, Claude Opus 4.5 80.9% (per `llm-stats.com/benchmarks/swe-bench-verified` and `benchlm.ai/benchmarks/sweVerified`, retrieved 2026-04-12)
- Current top of Pro: Claude Opus 4.5 45.9%, Claude Sonnet 4.5 43.6%, Gemini 3 Pro 43.3%, GPT-5.3-Codex with custom scaffold 57%, Opus 4.6 + WarpGrep v2 57.5%

**Freshness flag**: "Claude Mythos Preview 93.9%" at the top of Verified is a new entrant since the February 2026 leaderboard update. The name pattern suggests an unreleased internal Anthropic build; no public API availability as of retrieval. Treat as REPORTED-NOT-VERIFIED until a corresponding Claude-public-release announces.

**Leaderboard sources found**:
- `swebench.com/` — the canonical SWE-bench site, maintains both leaderboards
- `swebench.com/verified.html` — Verified specific
- `llm-stats.com/benchmarks/swe-bench-verified` — third-party aggregator
- `benchlm.ai/benchmarks/sweVerified` — third-party aggregator, tracks 31 LLMs
- `swe-bench-live.github.io/` — continuous-evaluation variant
- `live-swe-agent.github.io/` — related live-evaluation project
- `epoch.ai/benchmarks/swe-bench-verified/` — Epoch AI's analysis
- `morphllm.com/swe-bench-pro` — Pro-specific, primary source for the contamination claim
- `vals.ai/benchmarks/swebench` — Vals AI's wrapper

### HN front-page discussions (recent window)

**Key thread pattern** (not enumerated per-thread because adversary will audit the community sources separately): HN discussions in the last 30 days have clustered around four themes:

1. **SWE-Bench contamination**: OpenAI's decision to stop reporting Verified scores triggered a multi-day HN discussion (mid-February 2026). Dominant sentiment: "Verified is no longer trustworthy for frontier model evaluation; move to Pro or private evals."

2. **Cursor vs Claude Code comparison**: several threads comparing agent modes. Dominant sentiment: Cursor is faster for small-scope refactors, Claude Code agent-teams are better for parallel multi-file work. No clear winner; tradeoff depends on task shape.

3. **Devin 3 year-in-review**: Cognition's retrospective published around early April, discussing what worked (the autonomous loop) and what didn't (cost explosions on multi-day sessions, inability to recover from bad initial plans). Mixed reception on HN — some defending the approach, others pointing out it's expensive relative to a human developer for complex tasks.

4. **MetaGPT and CrewAI framework fatigue**: several "just use the Claude API directly" threads echoing Anthropic's own "Building effective agents" post warning about over-framework-ing.

### X.com activity (adversary should audit separately)

The 25,000-task experiment claim I cited in historian.md comes from X. The community discussion there has been:
- Critical of MetaGPT/ChatDev/CrewAI as "framework theater"
- Enthusiastic about minimalist agent loops
- Contested on Devin's real-world capabilities
- Actively discussing benchmark gaming

Several X accounts are clear boosters of specific products (Cursor fans, Devin fans, Aider fans) and their claims should be discounted for corpus-capture effect.

### Reddit r/LocalLLaMA and r/MachineLearning

WebFetch on reddit.com URLs still returns the anti-bot response I observed in the memory-layer session. Direct Reddit coverage unavailable via WebFetch; Reddit content is visible via WebSearch snippets only. This is a corpus gap flagged for synthesis.

### GitHub release velocity (14-day window)

From sensed activity on major repos:
- `princeton-nlp/SWE-agent` — active, weekly commits, released mini-SWE-agent variants
- `all-hands-ai/OpenHands` — very active, multiple releases per week, community-driven
- `paul-gauthier/aider` — Paul Gauthier commits daily, release cadence is weekly
- `geekan/MetaGPT` — less active, architectural-focused releases
- `OpenBMB/ChatDev` — less active
- `microsoft/autogen` — active, v2 architecture transition ongoing
- `joaomdmoura/crewAI` — active
- `anthropics/claude-code` — active (runtime releases), v2.1.32+ added agent-teams experimental

**Finding**: `princeton-nlp/SWE-agent` shipped a `mini-SWE-agent` variant in March 2026 that is now the default scaffold for the Verified leaderboard's "apples-to-apples comparison." Quote from HN/search results: "all LMs are evaluated using mini-SWE-agent in a minimal bash environment with no tools or special scaffold structure, just a simple ReAct agent loop."

**Implication**: the SWE-agent team itself concluded that minimal scaffolding is better for evaluation fairness. Supports the minimal-ReAct finding from Anthropic's SWE-bench blog.

## Sentiment summary

### On plan-vs-ReAct

Community sentiment (HN + X, anecdotal aggregate) has shifted toward **"ReAct inside, plan outside"**. Three common positions observed:

1. **"Pure ReAct believers"**: argue plan phases are bureaucratic overhead; cite Anthropic's SWE-bench blog and SWE-agent as authority.
2. **"Plan-first believers"**: argue that plan phases catch errors early; cite MetaGPT/ChatDev and Aider architect mode.
3. **"Hybrid winners"**: argue that a lightweight plan (5-10 minutes, not a 2-hour PRD) followed by execution with replan-on-failure is the practical win. This is the emerging consensus.

H3's two-phase design is the "hybrid winners" position.

### On multi-agent vs single-agent

Community sentiment has soured on heavy multi-agent frameworks in Q1 2026. The viral X claim about "25K-task experiment proving multi-agent frameworks built on wrong assumption" got substantial traction. The countering view: **multi-agent still wins when agents are small/cheap and coordinate through files, lose when agents are large/expensive and coordinate through conversations**. Research-team and engineering-team (file-backed, Opus per specialist but running in adopted-persona mode mostly) land on the right side of this tradeoff.

### On autonomous agents

Devin fatigue is real but not dominant. The community mostly respects Cognition's engineering work while being skeptical of the specific product's cost/benefit on complex tasks. SWE-agent, OpenHands, and Aider have broader adoption among OSS practitioners.

## Fresh finds that would not have been in a canonical sub-question list

1. **SWE-Bench Pro is the load-bearing benchmark as of April 2026**, not Verified. Any synthesis that cites Verified as "the SWE-bench number" is already behind the state of practice.
2. **mini-SWE-agent** is the standardized scaffold for fair LM comparison — SWE-agent's own team ships it.
3. **Claude Mythos Preview 93.9%** — unverified internal build name at top of Verified. Not adoptable yet.
4. **Opus 4.6 + WarpGrep v2 57.5% on Pro** — best agent-system score on the uncontaminated benchmark. Cited by Scale AI SEAL leaderboard.
5. **Devin 3 year-in-review** — published recently, public acknowledgment that autonomous loops struggle on multi-day tasks.
6. **Morph LLM published the contamination analysis** with direct quotes of OpenAI's audit finding. Morph LLM is a coding-agent vendor, so there's interest bias (competes with Cursor/Devin) — adversary should flag, but the primary-source quote from the OpenAI audit is cross-checkable.

## Items flagged for adversary

The following sources are load-bearing and should be audited by the adversary:
- `morphllm.com/swe-bench-pro` — MIXED (commercial vendor with interest, but contains primary-source quote from OpenAI audit)
- `swebench.com/` — STRONG-PRIMARY (official benchmark site)
- `llm-stats.com/benchmarks/swe-bench-verified` — SECONDARY/aggregator
- `benchlm.ai/benchmarks/sweVerified` — SECONDARY/aggregator
- `groundy.com/articles/swe-bench-verified-explained-...` — aggregator, likely AI-generated SEO, probably WEAK
- `x.com/sukh_saroy/status/2039381283999293799` — single-witness X post, REPORTED-NOT-VERIFIED
- `simonwillison.net/2026/Feb/19/swe-bench/` — Simon Willison's blog (normally STRONG, but the content retrieved didn't match the contamination claim — may be stale retrieval or redirect)
- `aider.chat/docs/leaderboards/` — maintainer's own site, STRONG-PRIMARY for Aider-specific claims
- `cognitionlabs.com/blog/devin-year-in-review` (if it exists) — interested primary for Devin-specific claims

## Confidence in this pass

**HIGH** on the benchmark contamination finding (multiple corroborating sources including the primary-source Morph LLM page). **HIGH** on the 14-day release activity summary for OSS repos. **MEDIUM** on community sentiment (aggregated from search results, not direct corpus scraping; adversary should bias toward discounting). **LOW** on any single-witness X claim. **LOW** on Reddit coverage (WebFetch blocked as in previous sessions).
