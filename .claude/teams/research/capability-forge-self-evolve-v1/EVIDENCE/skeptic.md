# Skeptic — reasoning attacks on the synthesis

Per MEMORY.md: skeptic attacks **reasoning**, adversary attacks **sources**. Running skeptic after adversary so that any source-level issues are already on the record. Dispatched to red-team the candidate synthesis and the moderator's REFRAME verdict.

## Attack 1 — "Wrap, don't rewrite" is assumptive

**The synthesis claim**: the Forge should wrap existing primitives (skill-creator, self-improving-agent, mcp-builder, MCP Registry) rather than reimplement them.

**The attack**: The cartographer inspected `self-improving-agent`'s SKILL.md and sub-skills on-disk but **never actually ran them end-to-end**. It's possible that:
- `/si:extract` requires MEMORY.md to be populated by Claude Code's auto-memory, not by programmatic writes. The Forge's curator pass would write to MEMORY.md but the extract pass might not see it if the path/format differs.
- `skill-creator`'s eval loop requires a human in the loop at multiple steps (per its SKILL.md: "Launch the viewer... tell the user... wait for the user"). A fully-autonomous Forge would be blocked waiting for human feedback on every iteration.
- `mcp-builder`'s "test via MCP Inspector" step requires interactive setup that a background Forge session can't do alone.

**Severity**: HIGH. If any of these are true, "wrap, don't rewrite" collapses and the Forge has to rebuild core machinery anyway.

**Resolution**: The Forge's first-session smoke test (§10 deliverable) must **actually invoke** at least one of these primitives end-to-end. If it can't complete the smoke test without manual intervention, the architecture must be revised in round 3 or in the next session.

**Downgrade**: the "wrap, don't rewrite" claim should be marked MEDIUM-HIGH confidence in SYNTHESIS, not HIGH.

## Attack 2 — The six roles may collapse into fewer in practice

**The synthesis claim**: Voyager (curriculum + skill library + iterative prompting) + ACE (Generator + Reflector + Curator) + Toolformer (value filter) = 6 roles for the Forge.

**The attack**: The six are derived from three different papers with three different problem framings. They don't necessarily compose cleanly:
- ACE's "Generator" overlaps heavily with Voyager's "iterative prompting mechanism" (both produce candidate behaviors).
- ACE's "Reflector" overlaps with Toolformer's filter (both judge whether a candidate is worth keeping).
- Voyager's "skill library" overlaps with ACE's "Curator" (both maintain a committed store).

**Possible real role count**: **3 roles**, not 6:
1. **Propose** (curriculum + generator + iterative drafting, all producing a candidate)
2. **Judge** (reflector + critic + value filter, all deciding whether to commit)
3. **Store** (skill library + curator, maintaining the committed corpus)

**Severity**: MEDIUM. Forces a cleaner sub-skill structure but doesn't change the architecture decision.

**Resolution**: Reduce the Forge's sub-skills from 6 to **4-5** (propose + judge + store + scout + maybe curriculum-specifically). The "scout" role (internet aggregation) is the only one that's genuinely distinct from Voyager/ACE because it wasn't in those papers — Akash added it as a requirement. Make scout a first-class sub-skill; collapse the rest.

**Revised sub-skill list for SYNTHESIS §1**:
1. `forge-gap` (curriculum: "what should we build next?") — inspects roster, diffs against community rosters, proposes.
2. `forge-scout` (internet aggregation: "what exists already?") — queries MCP Registry, anthropics/skills, installed marketplaces.
3. `forge-draft` (generator: "write the skill") — wraps skill-creator's authoring step.
4. `forge-test` (judge: "does it pass?") — wraps skill-creator's eval loop.
5. `forge-promote` (store: "commit to library") — writes SKILL.md to `~/.claude/skills/` and updates the Forge's MEMORY.md catalog.

5 sub-skills, one per concern. No double-duty. The 6th I originally considered (separate "scorer" for value tracking) can be a **hook** on session start that re-reads MEMORY.md counters — no dedicated sub-skill needed.

## Attack 3 — The moderator's REFRAME assumes H1→H2 is graceful, but what if it's not?

**The synthesis claim**: picking H1 now doesn't lock in single-agent forever; the upgrade to H2 is a local refactor.

**The attack**: The upgrade to H2 requires splitting one agent file into 5+ specialist files. But the specialist files need:
- Distinct `name` + `description` frontmatter (not a problem).
- Their own persona prose (a rewrite, not a copy — the single-agent prose blends perspectives that a specialist doesn't have).
- Their own tool allowlists (one-shot refactor, not clean diff).
- A PROTOCOL.md defining the dispatch order (new file, no precedent in H1).
- A shared workspace scaffold per session — the H1 Forge has NO per-session workspace; H2 needs one.

That's **not a local refactor**. It's a rewrite. The REFRAME verdict underplays the cost of the upgrade.

**Severity**: LOW-MEDIUM. Doesn't change the H1 decision for first session, but the "graceful upgrade" framing in the synthesis is optimistic.

**Resolution**: Rewrite the SYNTHESIS §1 "upgrade path" section to be honest: **"Start with H1. If the Forge proves valuable enough to warrant a team, a full rewrite to H2 is the path, not a local refactor."** This changes the psychology — the first H1 is a prototype, not a "forever" architecture.

## Attack 4 — The Forge may duplicate research-github-miner's work

**The synthesis claim**: the Forge's scout queries the MCP Registry routinely; research-github-miner is for deep/complex queries only.

**The attack**: In practice, **the MCP Registry query set is not bounded**. The Forge's scout will need to query for every possible capability category that a gap might fall into. That's the same API surface research-github-miner already owns. The split is artificial.

**Severity**: MEDIUM. If the split is artificial, the Forge and research-github-miner will step on each other in concurrent sessions.

**Resolution**: **Make scout a thin wrapper around research-github-miner's method, not a replacement.** The scout SKILL.md should explicitly say "for complex queries across multiple categories, delegate to research-github-miner via a research-request drop-file." The Forge's scout owns:
- **single-server lookups** (by name or exact-match search).
- **category-bounded listings** (one specific search term per query).
- **on-disk marketplace inventory** (Glob over `~/.claude/plugins/marketplaces/`).

The Forge's scout does NOT own:
- cross-roster competitive analysis (that's research-github-miner).
- sentiment trends (that's research-historian).
- SEO vetting (that's research-adversary).

## Attack 5 — The 5 first-batch skills may be wrong priorities

**The synthesis claim**: priorities are (1) HN MCP, (2) Semantic Scholar MCP, (3) arxiv MCP wrapper, (4) forge-curriculum, (5) forge-scout.

**The attack**: HN and Semantic Scholar MCPs are **library gaps**, not **workforce capability gaps**. Akash's research team already has WebFetch + web-miner for HN and Semantic Scholar. An MCP would be nice-to-have but is not load-bearing. Meanwhile, the **meta-orchestration category gap** (13 missing specialists per VoltAgent) is a much larger capability deficit that the Forge could start addressing via authored skills.

**Counter-argument to my own attack**: meta-orchestration is being addressed by the parallel `orchestration-full-activation-v1` session. The Forge should NOT duplicate that. So meta-orchestration is off-limits.

**Resolution**: The first-batch priorities should be the **intersection** of (a) capability gaps AND (b) not-being-addressed-by-another-in-flight-session AND (c) something the Forge can smoke-test in one session.

**Revised first-batch** (details in SYNTHESIS.md §4):
1. **`forge-gap`** sub-skill (implements gap detection — the Forge's own curriculum).
2. **`forge-scout`** sub-skill (wraps MCP Registry + disk inventory).
3. **Install arxiv MCP** (`blazickjp/arxiv-mcp-server`) — one-shot registry install, immediate value to research-lead's historian.
4. **Author `hn-search` skill** (not MCP — HN Algolia API via WebFetch is already viable; a skill that enshrines the query patterns is cheaper than an MCP).
5. **Author `semantic-scholar-search` skill** (same rationale).
6. **Author `registry-trust-heuristic` skill** (the 6-rule heuristic from adversary.md as a reusable reference skill).

Six items, not five. And MCPs are reduced from 2 to 0 — the Forge installs an existing one (3) and authors **skills** for the other two capabilities instead of MCP servers. This aligns with Pattern "default to skill" from librarian + Simon Willison.

## Attack 6 — The collaboration contract with research-lead is vague

**The synthesis claim**: the Forge delegates to research-lead via a file drop into `~/.claude/teams/research/inbox/`.

**The attack**: Does the research-lead polling protocol exist? **No.** The Research Team's current workflow is user-initiated per session. There's no inbox-polling. The Forge dropping a file won't trigger anything.

**Severity**: HIGH — this is a hole in the collaboration contract.

**Resolution**: The collaboration contract must specify either:
- **User-mediated handoff**: the Forge writes to `~/.claude/forge/research-requests/<slug>.md` and **stops**. The file's existence is a signal for Akash (or the main session) to manually invoke `research-lead` with the request as the prompt.
- **OR** (harder): add a hook (PreSessionStart?) that scans the research-requests directory and includes pending requests in the research-lead's session start context. This is more automated but requires Akash to enable a hook.

Choose the user-mediated handoff for §6 of SYNTHESIS. It's simpler, testable, and doesn't depend on hook infrastructure the Forge can't guarantee.

## Attack 7 — "User-invocable: false" reference skills may be underused

**The synthesis claim (from linguist)**: use `user-invocable: false` for Forge's reference skills (like the agent catalog, trust heuristic).

**The attack**: this is the right frontmatter, but **a reference skill Claude never loads is zero-value**. Claude only loads skills when the description matches a session's context. The Forge's reference skills would be loaded only when a session is *already* authoring a skill or investigating a registry entry. But the Forge is the only agent that does that — and the Forge is a single specialist. So the reference skills would only be loaded when the Forge itself is invoked.

**Is that a problem?** No — that's the intended design. But the synthesis should make this explicit: **reference skills are ONLY loaded when the Forge itself runs. They are Forge-internal context, not general-purpose.** Document this explicitly in the sub-skill frontmatter: use `paths:` glob patterns to restrict loading to Forge's own workspace OR add an explicit "only use this skill when running as forge-lead" directive in each sub-skill's description.

**Severity**: LOW — documentation issue, not architectural.

**Resolution**: Add a clarification to SYNTHESIS §3 (Skill authoring protocol) — the Forge's sub-skills use **narrow triggering scope**, not pushy descriptions. Claude should NOT auto-load them in general sessions, only when the Forge is explicitly running. Use either `paths: ["~/.claude/forge/**"]` (if the Forge session always cwds into its own dir) or `disable-model-invocation: true` (manual invocation only).

## Attacks rejected

- **"The Forge is unnecessary because skill-creator already exists"** — rejected. Skill-creator is a reactive skill authoring harness; the Forge is a proactive gap-detecting and self-improving meta-system. They have different purposes even though they compose.
- **"All Opus max effort means H1 is overkill because a single Opus can do everything"** — rejected. Akash's doctrine is max effort, but that's about *quality*, not *scope*. A single-agent at max effort still has context limits and coherence costs if you pile too many responsibilities on one prompt.

## Skeptic's summary

Four attacks produced actionable resolutions:
- **#1** → downgrade "wrap, don't rewrite" to MEDIUM-HIGH; §10 smoke test must actually run one primitive end-to-end.
- **#2** → reduce 6 sub-skills to 5 (propose/scout/draft/test/promote), collapse value-tracking into a start-of-session hook.
- **#3** → be honest that H2 upgrade is a rewrite, not a refactor.
- **#4** → scout is a thin wrapper; explicit bounded ownership with research-github-miner.
- **#5** → first-batch priorities are 1 install + 3 skills + 2 Forge-internal sub-skills, not 2 MCPs.
- **#6** → user-mediated research handoff, not automatic polling.
- **#7** → narrow triggering scope on Forge sub-skills, not pushy descriptions.

Five claims were overstated in the candidate synthesis. **None of the attacks break the architecture** — H1 is still the right call, and the moderator's REFRAME verdict stands. But the synthesis must be written with the corrections above baked in.

Confidence after skeptic pass: **HIGH on architecture (H1 with upgrade path), HIGH on reuse pattern, HIGH on collaboration contract (user-mediated), MEDIUM on "wrap, don't rewrite" pending smoke test, HIGH on the 5-sub-skill decomposition**.
