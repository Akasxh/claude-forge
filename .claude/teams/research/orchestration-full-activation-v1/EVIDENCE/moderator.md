---
specialist: research-moderator
slug: orchestration-full-activation-v1
started: 2026-04-12T07:50Z
completed: 2026-04-12T08:00Z
tool_calls_count: 3
citations_count: 11
confidence: high
---

# Moderator — 3-round structured debate on C1 (hook enforceability)

Contradiction (from synthesist): Is H3 (PreToolUse hook blocking SYNTHESIS.md
writes when evidence audit fails) implementable in Claude Code v2.1.101 today,
or does the enforcement protocol need to depend on lead-discipline via Bash
audit calls?

## Method

3-round structured debate per DebateCV pattern (arxiv 2507.19090, cited in
PROTOCOL.md). Two debaters present first-party evidence; I, the moderator,
drive 3 rounds of claim + counter-claim + resolution. Verdict types from
memory-layer session's lesson 10: {A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER}.

## Sides

**Side L (Librarian)**: H3 works per primary-source docs.
- Evidence: code.claude.com/docs/en/hooks Subagent Tool Call Filtering table,
  PreToolUse input schema including `agent_id`/`agent_type`, frontmatter
  `hooks:` block support, "exit code 2 blocks the tool call" semantics.
- Position: the docs are the contract. If implementing them is a runtime
  bug, that's a bug to file, not a design constraint.

**Side G (GitHub-miner)**: H3 does NOT work for subagents in current runtime.
- Evidence: 8+ OPEN issues filed against anthropics/claude-code between
  2026-01-15 and 2026-04-10, reporting PreToolUse hooks silently disabled
  for subagents. Root cause traced by a community reporter into cli.js v2.1.92:
  `_R()` has `if (U6(process.env.CLAUDE_CODE_SIMPLE)) return;` that
  short-circuits the hook runner in subagent context. Under
  `bypassPermissions` mode (Akash's default), hooks are entirely bypassed
  for subagent tool calls per issue #43772.
- Position: the runtime is the ground truth; building on documented-but-
  unimplemented behavior is reckless.

## Round 1 — opening arguments

### L-1 (librarian's opening)

> "I cited 22 verbatim passages from `code.claude.com/docs/en/hooks`, `/sub-agents`,
> `/agent-teams`, `/settings`, and `/permissions`. Every one of them was
> retrieved 2026-04-12, within 24 hours of this session. The `agent_id` field
> IS in the PreToolUse input schema. The `Subagent Tool Call Filtering` section
> describes a standard pattern using that field. The 'exit code 2' table shows
> PreToolUse can block.
>
> Moreover, the `~/.claude/settings.json` PreToolUse(Bash) hook that Akash
> already has working (for `git-identity.sh` on git commit/push) proves
> the hook mechanism is live. I did the cross-check: the existing hook's
> JSON syntax matches the docs exactly.
>
> If runtime issues exist, they should be filed and fixed. We should not
> design backwards from a bug."

### G-1 (github-miner's opening)

> "I read the raw GitHub issues, sorted by recency. Eight issues, seven of
> them still OPEN, all filed in the 90 days preceding this session. Issue
> #43612 (filed 2026-04-04, v2.1.92) has a community reporter who *extracted
> and read cli.js from the npm package* and found the exact lines of code
> causing the silent no-op:
>
> ```javascript
> async function*_R({hookInput, toolUseID, matchQuery, signal, ...}) {
>     if (S18()) return;                                // disableAllHooks policy
>     if (U6(process.env.CLAUDE_CODE_SIMPLE)) return;   // THIS LINE
>     ...
> }
> ```
>
> This is not speculation. This is a line-number-level trace into the shipping
> runtime. The `_R()` function — the universal hook runner — bails out when
> `CLAUDE_CODE_SIMPLE` is truthy in the subagent's environment. Per the
> reporter, subagents run with this env var set by the runtime, not by user
> choice. The hook is called; it returns; its side-effects are skipped.
>
> Issue #43772 (filed 2026-04-05) is worse: under `bypassPermissions` mode,
> hooks for subagents are bypassed entirely. The reporter documented 3
> unauthorized git commits, 7 file deletions, and chmod +x calls that their
> allowlist hook should have blocked.
>
> Issue #40580 (filed 2026-03-29) is worse still: the hook IS called, returns
> exit 2, and **the runtime ignores the exit code**. The block never happens.
>
> The current Claude Code version we're running is v2.1.101 — 9 patches ahead
> of v2.1.92, and there's no changelog evidence these bugs are fixed."

### Moderator Round 1 summary

Both sides present primary-source evidence. Both sources are authoritative
within their own truth-conditions:
- Librarian: Anthropic's published contract.
- GitHub-miner: community-reproduced runtime behavior.

The contradiction is NOT at the evidence layer; it's at the truth-value
layer. "Docs say X" and "runtime does not X" are both true.

## Round 2 — direct exchanges

### L-2 (librarian responds)

> "Fine, the runtime has bugs. But two things:
>
> 1. The main-thread PreToolUse hook DOES work reliably — Akash's existing
>    git-identity.sh hook proves it. Main-thread enforcement is a subset of
>    H3 that IS implementable today.
>
> 2. PostToolUse hooks for subagents DO fire in v2.1.89+ per issue #34692
>    comment from user `prodan-s`. So H3-observational (non-blocking audit
>    logging) is implementable today, just not H3-blocking.
>
> The correct framing is that H3 is a LAYERED design, not a single-mechanism
> design. Some layers work; some don't. Adopt the ones that do.
>
> Do NOT adopt:
> - PreToolUse on subagent Write blocking SYNTHESIS.md writes
>   (broken for subagents, especially under bypassPermissions)
>
> DO adopt:
> - PreToolUse on main-thread Write — works
> - PostToolUse on subagent Write/Edit for observational logging — works
>   in v2.1.89+
> - Stop hooks on research-lead's final turn (main thread) — worth testing
>
> The docs are 'aspirationally complete' today. Over time they converge with
> the runtime. Our design should target the layer that IS shipping."

### G-2 (github-miner responds)

> "Agreed with layered framing. I'd push further: for Akash's specific
> configuration (`bypassPermissions: 'default'`) the main-thread/subagent
> distinction matters more than usual because `bypassPermissions` is the
> mode that most aggressively breaks hooks for subagents.
>
> I'd argue we should NOT build any enforcement gate on hooks, even the
> PostToolUse observational layer, BECAUSE:
>
> 1. The docs-vs-runtime gap is WIDE (8 open issues, one with cli.js root-
>    cause trace). We can't trust any hook claim.
> 2. The `_R()` guard checks `CLAUDE_CODE_SIMPLE` globally. There's no
>    published fix; may affect PostToolUse as well as PreToolUse in
>    future versions.
> 3. The lead-discipline Bash-audit-call path is runtime-independent. It
>    works regardless of what the hook subsystem does.
>
> Build on the most reliable substrate, not the most documented one."

### Moderator Round 2 summary

L-2 and G-2 converge on: H3 is layered. They differ on: should we use ANY
hooks for enforcement?

L-2 position: use PostToolUse for non-blocking observational logging because
it's reported working in recent versions.

G-2 position: use NO hooks for enforcement; lean entirely on lead-discipline
Bash calls for both enforcement AND logging (the lead can tail the audit log
itself via Bash).

This is a **real design tradeoff**, not a factual disagreement. Both sides
agree on what works and what doesn't. They differ on whether to depend on
the "works in recent versions" layer (PostToolUse) at all.

## Round 3 — resolution attempt

### L-3

> "Dependency on PostToolUse is cheap to write and cheap to remove. If the
> hook pipeline breaks in v2.1.102 for PostToolUse too, we lose the
> observational log but the primary enforcement (H1 lead-discipline) is
> still intact. The cost of adoption is low; the benefit is a timestamped
> audit trail with agent context that we couldn't construct otherwise.
>
> This is graceful degradation: build the PostToolUse layer, label it
> 'best-effort observational', accept that it may not fire in all
> environments. The PRIMARY enforcement does NOT depend on it."

### G-3

> "If it's clearly labeled as best-effort observational and the retrospector
> does NOT require its output to grade a session, I agree.
>
> Two concrete safeguards:
>
> 1. `log-evidence-writes.sh` must ALSO be invocable by the lead via Bash
>    with synthetic input (i.e., it's a script that the lead can call in
>    a test harness, not just a runtime hook). The empiricist already did
>    this; extend it to production use.
>
> 2. The retrospector's close-audit must NOT fail a session on missing
>    audit log entries. It grades compliance (audit called before
>    SYNTHESIS?) as a SOFT signal, not a HARD gate.
>
> With those two, I withdraw my objection."

### L-3 accepts G-3's safeguards

> "Both safeguards are fine. Let's lock the verdict."

## Moderator's verdict: **REFRAME + COMPLEMENTARITY**

The question "does H3 work today" was mis-posed. The corrected framing:

> **H3 is a layered enforcement design. Some layers are implementable today
> via current runtime primitives (main-thread PreToolUse, PostToolUse on
> subagent Write/Edit in v2.1.89+); other layers are NOT implementable
> today due to documented-vs-actual runtime bugs (PreToolUse blocking on
> subagent tool calls, especially under bypassPermissions). Adopt the
> implementable layers as auxiliary observational mechanisms. Rely on
> lead-discipline Bash audit calls (H1) as the primary enforcement path
> because it is runtime-independent.**

### Adopted layers

1. **H1 lead-discipline Bash audit call** (PRIMARY, always required):
   `bash -c 'python3 ~/.claude/scripts/audit_evidence.py <slug>'` at
   the mid-flight and synthesis gates. Runtime-independent.

2. **H3 PostToolUse observational logging** (AUXILIARY, best-effort):
   `~/.claude/hooks/log-evidence-writes.sh` invoked by PostToolUse hook
   on `Write|Edit` matcher in `~/.claude/settings.json`. Non-blocking.
   Writes to `<workspace>/_write_audit.log` for retrospector to read.
   Best-effort per github-miner's issue survey (may silently no-op in
   some version ranges).

3. **Main-thread PreToolUse hook** (OPTIONAL, future work): when the
   main session (not a subagent) writes SYNTHESIS.md, a PreToolUse hook
   CAN block it pending audit. Main-thread hook is reliable per Akash's
   existing git-identity.sh proof. But: the research-lead runs as a
   subagent in the default Akash setup, so this layer doesn't apply to
   the primary code path. Optional v2.2 addition if main-thread lead
   invocation becomes the default.

### Rejected layers

- PreToolUse blocking on subagent tool calls: broken per github-miner
  §1-2. Revisit when Anthropic closes issues #43612, #43772, #40580.
- PreToolUse `permissionDecision: deny` JSON output: broken for Agent
  tool calls per issue #44534.
- Subagent frontmatter `hooks:` block: unreliable per issue #27755, #18392.

### Safeguards (from G-3)

1. `log-evidence-writes.sh` must be invocable from Bash with synthetic
   input for testing. (Already implemented by empiricist §E_a.)
2. Retrospector's close-audit grades compliance as a SOFT signal, not a
   HARD gate. A session can close without an audit-log entry if the
   main enforcement (H1 Bash calls) ran.

## Citations

- [MOD1] librarian.md §1-2 (primary-source Anthropic docs verbatim)
- [MOD2] librarian.md §11 (version caveats, existing hook cross-check)
- [MOD3] github-miner.md §1 (issue #43612 _R() line-number trace, 2026-04-04)
- [MOD4] github-miner.md §1 (issue #43772 bypassPermissions bypass, 2026-04-05)
- [MOD5] github-miner.md §1 (issue #40580 exit 2 ignored, 2026-03-29)
- [MOD6] github-miner.md §1 (issue #34692 comment v2.1.89+ PostToolUse working)
- [MOD7] github-miner.md §1 (issue #44534 permissionDecision deny broken)
- [MOD8] github-miner.md §5 (summary table of runtime reality vs docs)
- [MOD9] empiricist.md §E_a (hook dry-run script + synthetic input pattern)
- [MOD10] tracer.md §2 (v2.1 counterfactual against engineering session)
- [MOD11] linguist.md §3 (terminology lock: "observational hook" vs "blocking hook")

## Handoffs

**For synthesist**: update claim matrix to mark C1 as RESOLVED via REFRAME
+ COMPLEMENTARITY. Both sides contributed load-bearing constraints; the
winning design uses both.

**For skeptic**: attack the safeguards. Is "best-effort observational hook"
+ "soft-signal retrospector grade" really enforcement, or does it collapse
back to lead-discipline-only because the auxiliary layer is unreliable?

**For the lead (Synthesis-level)**:
- **Primary enforcement layer**: H1 lead-discipline Bash audit calls at
  mid-flight and synthesis gates.
- **Auxiliary observational layer**: PostToolUse hook `log-evidence-writes.sh`
  for timestamped audit trail. Best-effort.
- **NOT in the design**: PreToolUse blocking on subagent tool calls.
- **Smoke test**: the positive control is the engineering-team-self-evolve-v1
  session (260KB, 16/17, PASS). Negative control is SMOKE_TEST_shortcut
  (272 B, 2/17, FAIL with 23 violations). Both are already built.

## Confidence

**HIGH** on the reframe verdict — both sides explicitly accepted after G-3's
safeguards were added. No further debate needed. Complementarity is the right
technical term: both contributions are present in the final design, one as
primary, one as auxiliary.
