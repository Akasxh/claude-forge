# QUESTION.md — claude-memory-layer-sota-2026q2

**Session start**: 2026-04-12
**Lead**: research-lead (adopted-persona mode, sub-dispatch not available)
**Slug**: `claude-memory-layer-sota-2026q2`
**Protocol**: v2 (first live pilot on a real question)

## Raw prompt (verbatim from Akash, 2026-04-12)

> "Research how we can have a memory layer for Claude. Something more than
> just SQL or something. Something latest, as recent as today."

## Assumed interpretation

Akash is not asking about key-value persistence. He is running a heavy Claude
Code setup with a custom multi-agent Research Team and already uses the
Claude Code built-in `memory: user` file-injection mechanism (that is how
`~/.claude/agent-memory/research-lead/MEMORY.md` gets seeded into this very
session). So "something more than SQL" means:

**What is the state-of-the-art memory architecture for LLM agents in
2025-2026, and what could Claude Code's memory story look like beyond
the current 25KB-file-dump model?**

The audience is a builder. He wants a concrete architecture he can adopt
or implement this quarter, not a menu of nine options.

## Context signals used for the interpretation

1. `cwd: /home/akash/PROJECTS/claude` — an active Claude Code customization
   project, not a user-facing app.
2. `~/.claude/agents/research/` holds 19 freshly-built specialists wired
   for the v2 protocol, meaning he cares about multi-agent infrastructure.
3. `~/.claude/agent-memory/research-lead/MEMORY.md` is 7260 bytes of
   durable session lessons written by the retrospector — Akash already
   uses the "memory as evolving playbook" pattern.
4. He explicitly said "as recent as today" — 2026-04-12 cutoff, prefer
   primary sources from the last 12 months.
5. He said "something more than SQL" — he knows SQL/KV already and wants
   us to look past it.

## Sub-questions

1. **SOTA landscape**: What memory architectures are published in
   2025-2026 literature beyond RAG-over-SQL? Episodic vs semantic vs
   procedural memory, hierarchical memory, vector-native, temporal
   knowledge graphs, hippocampal-inspired, compressive-transformer-state,
   playbook-as-memory, in-context memory, test-time adaptation.

2. **Production systems**: What does Mem0, Zep, Letta/MemGPT, Memary,
   Cognee, LangMem, Graphiti, OpenAI memory, Claude's own memory, Gemini
   memory, character.ai memory actually do under the hood? Which primitives
   do they share and where do they diverge?

3. **Claude Code's current mechanism**: Document the actual `memory: user`
   file-injection behavior and its limits (25KB, 200-line, no vector
   search, no temporal queries, no entity graph, no reflection loop).

4. **Failure modes**: What does the literature say goes wrong with memory
   layers in production? Context rot, memory hallucination, retrieval-
   augmented-poisoning, write amplification, staleness, context-window
   pollution, forgetting calibration, polysemous-key collisions.

5. **Academic 2025-2026 primary sources**:
   - Letta/MemGPT (self-edit loop, arxiv 2310.08560 + follow-ups)
   - A-MEM (arxiv 2502.12110 / Xu et al.)
   - Mem0 paper (arxiv 2504.19413 / Chhikara et al.)
   - Memory in the Age of AI Agents (arxiv 2512.13564-ish, verify)
   - HippoRAG / HippoRAG 2 (arxiv 2405.14831 / 2502.14802)
   - SCM (Self-Controlled Memory, arxiv 2304.13343)
   - MemoryBank (arxiv 2305.10250)
   - ACE: Agentic Context Engineering (arxiv 2510.04618)
   - Generative Agents memory stream (Park et al. 2023) — foundational
   - Reflexion memory (Shinn et al. 2023) — foundational

6. **Architecture synthesis**: What would a "something more than SQL"
   memory layer for Claude Code look like concretely? Components: store,
   index, retriever, writer, curator, reflector, injection-policy. Which
   SOTA technique owns each component?

7. **Tradeoffs**: Cost / latency / accuracy / local-first / privacy /
   operational-complexity across approaches.

8. **Recommendation**: Given Akash's constraints (local-first, privacy,
   all-Opus, file-system-as-state, Claude Code integration, max-effort
   quality), which approach wins and why? Must be "do X with Y" not
   "here are options."

## Constraints

- Cutoff: 2026-04-12. Prefer sources from last 12 months.
- No hand-waving. Every benchmark claim needs a primary source OR an
  explicit "unverified / marketing" flag.
- Local-first: Akash's setup runs on his machine, not a cloud service.
- Privacy: no third-party calls we would not be comfortable shipping.
- Recommendation must be actionable this week.
- The adversary gate is load-bearing here — "AI memory" is one of the
  most SEO-gamed topics of 2025-2026. Every marketing benchmark audited.

## Definition of done

A PASS from `research-evaluator` on all 5 rubric dimensions, plus:
- A concrete recommendation (component-by-component)
- 15+ primary sources cited (papers, official docs, release notes)
- Adversary's corpus verdict "healthy" or "mixed" — not "compromised"
- Retrospector writes durable lessons about running v2 on a
  heavily-SEO-gamed topic

## Acceptance criteria

- Architecture sketch with store / index / retriever / writer / curator /
  reflector / injector for the concrete recommendation.
- Evaluator PASS verdict on all 5 rubric dimensions OR a PROVISIONAL
  with explicit "what would turn it into PASS".
- Retrospector's lessons written to MEMORY.md and deduped by scribe.
