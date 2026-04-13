# Retrospector — session post-mortem and lessons for MEMORY.md

Session: `capability-forge-self-evolve-v1`
Closed: 2026-04-12, after 1 round 1 (wide) + round 2 (synthesist + moderator + skeptic + adversary + evaluator) + final SYNTHESIS.md.

## Outcome

PASS (HIGH confidence, conditional on §10 smoke test validating the "wrap, don't rewrite" claim).

All 10 deliverables written verbatim in SYNTHESIS.md. Architecture decision bound (H1 with upgrade path). Five sub-skill SKILL.md files fully drafted in §2 with frontmatter and body ready to `Write`. First-batch priorities ranked. Collaboration contract specified. Workspace layout finalized at `~/.claude/forge/`.

## New lessons distilled for `~/.claude/agent-memory/research-lead/MEMORY.md`

### Lesson 12: **"Wrap, don't rewrite" is the default pattern for meta-tooling sessions**

- **Observed in**: capability-forge-self-evolve-v1 (2026-04-12) — session discovered on-disk reference implementations for every major Forge responsibility (skill-creator for authoring, self-improving-agent for extraction, mcp-builder for MCP creation, MCP Registry for discovery).
- **Failure mode addressed**: architectural over-engineering (not a MAST failure directly, but close to FM-1.1 scope inflation).
- **Lesson**: when the user asks to design a meta-capability (tool builder, code generator, skill forge, plugin authoring system), the first round must **inventory existing primitives exhaustively** before proposing architecture. In the Forge session, 4 primitives were already on disk (skill-creator, self-improving-agent, mcp-builder-reachable, MCP Registry). Once those were discovered, the architecture collapsed from H2 (mini-team) to H1 (single agent with sub-skills that wrap the primitives). The on-disk inventory saved ~4x implementation effort.
- **Rule of thumb**: for meta-tooling research sessions, dispatch cartographer + librarian + github-miner in the *opening round* with explicit "find existing implementations" sub-questions, and delay the architecture debate until round 2 after the inventory returns. Assumption-first architecture design on meta-tooling is premature.
- **Counter-example / bounds**: for genuinely novel tooling (where no primitive exists), inventory yields nothing and the debate has to proceed on theory. In that case, cite the theory papers (Voyager, ACE, Toolformer) explicitly as the substrate and mark the architecture as "no-precedent, propose-and-iterate."

### Lesson 13: **Agent Teams is a real 2026 experimental primitive — distinct from subagents, distinct from teams-as-file-pattern**

- **Observed in**: capability-forge-self-evolve-v1 (2026-04-12) — librarian's redirect-follow on `code.claude.com/docs/en/sub-agents` surfaced a "see agent teams instead" note; web-miner fetched the full `code.claude.com/docs/en/agent-teams` doc and confirmed the experimental flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, version gate v2.1.32+, runtime state paths at `~/.claude/teams/<team-name>/config.json` and `~/.claude/tasks/<team-name>/`.
- **Failure mode addressed**: FM-1.1 (task specification via outdated knowledge).
- **Lesson**: Claude Code's 2026 primitive stack is (experimental) **Agent Teams** — cross-session parallel collaboration with shared task list + mailbox + hooks. Distinct from subagents (within-session delegation). **Akash's existing `~/.claude/teams/research/` workspace pattern is file-based and coincidentally uses the same top-level directory as the experimental runtime — this is a potential collision.** The Research Team's file layout (`teams/research/PROTOCOL.md`, `teams/research/<slug>/*`) is NOT incompatible with the runtime (which uses `teams/<team-name>/config.json`), but it's close.
- **Rule of thumb**: when designing a new team, research the Claude Code runtime docs for the primitive first. Check whether the team pattern is file-based (like Research Team v2) or runtime-backed (Agent Teams). Document which in the team's PROTOCOL.md. If a team will eventually upgrade to runtime-backed, plan the migration path from day 1.
- **Counter-example / bounds**: for a team whose coordination is inherently in-process (like single-session parallel dispatch), Agent Teams is overkill — subagents or file-based teams are the right primitive.

### Lesson 14: **"REFRAME" verdict works when the question collapses to "when" instead of "which"**

- **Observed in**: capability-forge-self-evolve-v1 (2026-04-12) — moderator ran a 3-round debate on H1 vs H2 and reframed to "H1 now, H2 later on workforce scaling trigger". The reframe was not a dodge — it was the honest answer once both sides' arguments were on the table. Neither H1 nor H2 was wrong; they were **ordered in time**.
- **Failure mode addressed**: FM-2.3 (task derailment by forcing a winner-take-all verdict when the real answer is "both").
- **Lesson**: REFRAME verdicts are appropriate when the question classifies two positions as "alternatives" but the positions are actually "sequential stages of the same system." The moderator's job is to detect this and reframe to the ordering question ("when should we switch?") instead of the competition question ("which is right?").
- **Rule of thumb**: in a moderator debate, before calling A_WINS or B_WINS, ask: "is one of these the early-stage and the other the late-stage of the same system?" If yes, REFRAME to the trigger conditions for the transition.
- **Counter-example / bounds**: when the two positions are genuinely incompatible (different file formats, different runtime models, etc.), REFRAME is a dodge and the debate must force a decision.

### Lesson 15: **Parallel research sessions must read each other's INDEX.md to avoid capability-gap duplication**

- **Observed in**: capability-forge-self-evolve-v1 (2026-04-12) — the Forge session identified meta-orchestration as VoltAgent's biggest gap category (13 missing specialists), but the parallel `orchestration-full-activation-v1` session is addressing exactly that category. If the Forge had not known about the parallel session, it would have proposed to fill the meta-orchestration gap itself, duplicating work.
- **Failure mode addressed**: FM-1.3 (step repetition across sessions).
- **Lesson**: when multiple research sessions run in parallel (Akash's current state: 4 sessions on 2026-04-12), each session must read `~/.claude/teams/research/INDEX.md` AND the other sessions' `QUESTION.md` files at round 0 to identify scope overlaps. Forge learned this ad-hoc by noticing the orchestration session in its own brief; a future meta-protocol should make this mandatory.
- **Rule of thumb**: at session start, after reading MEMORY.md, the research-lead must run a "parallel sessions check" — Glob `~/.claude/teams/research/*/QUESTION.md` for any session dated within 24h, read the Assumed Interpretation sections, and explicitly flag in QUESTION.md which in-flight sessions own which scope.
- **Counter-example / bounds**: for solo research sessions (no parallels), this check is a no-op.

### Lesson 16: **ACE-style bulleted memory with counters is the canonical long-term pattern for agent playbooks**

- **Observed in**: capability-forge-self-evolve-v1 (2026-04-12) — the Forge's MEMORY.md schema was derived directly from ACE (arxiv 2510.04618), which has primary-source support AND matches the de-facto structure of Akash's existing research-lead MEMORY.md.
- **Failure mode addressed**: cross-session learning gap (not a MAST mode).
- **Lesson**: every agent persona with a persistent MEMORY.md should use the ACE schema: bulleted entries with unique ID + helpful_count + harmful_count + content. Rewriting in-place loses detail (ACE's "context collapse"); summarizing loses nuance (ACE's "brevity bias"). Append-with-counters is the winning pattern per the paper's ablation. Research-lead's MEMORY.md currently uses ACE-adjacent format (titled lessons with observation/failure-mode/rule/counter-example); formalize that as the standard for all future agent memory files.
- **Rule of thumb**: any new agent memory file (forge-lead, engineering-team-lead, etc.) should use the same schema: lesson title → observation → failure mode → lesson body → rule of thumb → counter-example/bounds. This is the research-lead schema Akash already uses, which is an ACE implementation.
- **Counter-example / bounds**: for one-shot sessions (memory not persistent), ACE is overkill. But every team with cross-session learning benefits.

## Process improvements for the next Forge-like session

1. **Skip the 6-role Voyager+ACE+Toolformer composite exposition** — it's nice theory but skeptic attack #2 collapsed it to 5 roles. Start with the 5-role decomposition and cite the papers in support, not as the primary framing.
2. **Check installed plugins FIRST** — before any architecture debate, read `installed_plugins.json`. Akash often already has the primitive someone is about to propose reinventing.
3. **Read on-disk marketplaces systematically** — the alirezarezvani `self-improving-agent` reference would have been found 30 minutes earlier if the cartographer had specifically Globbed `~/.claude/plugins/marketplaces/*/engineering-team/*/SKILL.md` in round 1 instead of waiting for the ad-hoc discovery.
4. **The file-drop research-request protocol is underdesigned** — it works for this session, but a future agent orchestrator should formalize it. Flag for the orchestration session.

## Files appended to MEMORY.md

Lessons 12-16 above will be appended by the scribe to `~/.claude/agent-memory/research-lead/MEMORY.md`. The Forge's own memory file at `~/.claude/agent-memory/forge-lead/MEMORY.md` will be seeded with the §7 template content from SYNTHESIS.md when the executor writes the Forge.

## Self-check

- Did the session answer the user's question? **Yes** — all 10 deliverables written.
- Did it use the fewest rounds possible? **Yes** — 2 rounds (wide + synthesis+gates), no round-3 empiricist call because no testable hypothesis surfaced that a smoke test can't resolve.
- Did it introduce any lessons that should be binding on future sessions? **Yes, 5 lessons (12-16)**.
- Did any specialist fail to write their evidence file? **No, all 11 evidence files written**.
- Did the moderator run without bias? **Yes — the REFRAME verdict was reached by letting both sides argue in 3 rounds, then synthesizing the "ordered in time, not competing" reframe. Documented in `EVIDENCE/moderator.md` with round-by-round arguments.**
- Did the adversary clear all primary sources? **Yes — every STRONG-PRIMARY source verified, every MIXED source tiered, two REPORTED-NOT-VERIFIED labels applied correctly.**
- Did the evaluator pass the 5-dim rubric? **Yes — 4/5 green at synthesist time, 5/5 green after SYNTHESIS.md written.**

Retrospector closes.
