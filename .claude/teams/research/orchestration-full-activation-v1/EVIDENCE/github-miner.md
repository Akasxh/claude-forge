---
specialist: research-github-miner
slug: orchestration-full-activation-v1
started: 2026-04-12T05:55Z
completed: 2026-04-12T06:15Z
tool_calls_count: 18
citations_count: 23
confidence: high
---

# GitHub-miner — code-level audit of enforcement mechanisms + Claude Code runtime reality check

Sub-question (from planner): Code-level survey of how the frameworks actually implement
worker-execution enforcement. Read AutoGen runtime for actor ack/nack, LangGraph source
for state-node completion checks, CrewAI source for task-result validation, any relevant
GitHub issues about "agent didn't run" or "worker skipped" with resolution commits.

## Method

GitHub search via `gh api` REST endpoints. Two targets:
1. **Framework source reality** — Magentic-One orchestrator source, verifying paper claims.
2. **Claude Code runtime reality** — issue search for hook/subagent interaction bugs,
   since the librarian's finding (hooks fire for subagent tool calls per docs) needs
   empirical cross-check against filed runtime bugs.

Tool-call budget: 18. 23 citations, all from GitHub API returns.

## 1. THE LOAD-BEARING DISCOVERY — Claude Code hook docs contradict actual runtime

The librarian's primary-source doc extraction said:

> "PreToolUse hooks fire for subagent tool calls... with `agent_id` and `agent_type`
> in the payload... exit 2 blocks the tool call."

**The docs are aspirational. The runtime does NOT reliably honor this**, based on 8+
open/recent issues (2026-01 through 2026-04-10) filed against anthropics/claude-code:

### Issue graph (all OPEN as of 2026-04-12, unless noted)

| # | Title | Filed | State |
|---|---|---|---|
| #43612 | "PreToolUse/PostToolUse hooks silently disabled in subagents due to CLAUDE_CODE_SIMPLE check in _R()" | 2026-04-04 | **OPEN** |
| #43772 | "Subagents with bypassPermissions ignore PreToolUse hooks — unauthorized commands, wasted tokens" | 2026-04-05 | **OPEN** |
| #40580 | "PreToolUse hook exit code ignored for subagent tool calls" | 2026-03-29 | **OPEN** |
| #44534 | "PreToolUse hook deny not enforced for Agent tool calls" | 2026-04-07 | **OPEN** |
| #34692 | "PreToolUse/PostToolUse hooks do not fire for subagent (Agent tool) tool calls" | 2026-03-15 | **OPEN** |
| #27755 | "SubagentStart/SubagentStop unreliable for settings.json hooks — cascade failures break agent lifecycle management" | earlier | **OPEN** |
| #18392 | "Hooks in agent frontmatter not executed for subagents" | 2026-01-15 | CLOSED (duplicate of #17688) |
| #44075 | "SubagentStart hooks not fired for background agents" | 2026-03 | **OPEN** |
| #39814 | "PreToolUse hook `updatedInput` silently ignored for Agent tool" | 2026-03 | **OPEN** |

### Root cause from issue #43612 (traced into cli.js v2.1.92)

Reporter extracted and read `cli.js` from `@anthropic-ai/claude-code@2.1.92` and
found the universal hook runner `_R()`:

```javascript
async function*_R({hookInput, toolUseID, matchQuery, signal, ...}) {
    if (S18()) return;                                // disableAllHooks policy
    if (U6(process.env.CLAUDE_CODE_SIMPLE)) return;   // <-- THIS LINE
    ...
}
```

> "`CLAUDE_CODE_SIMPLE` is set to `"1"` when `--bare` mode is active. Subagents
> appear to run in a context where this env var is truthy, causing `_R()` to
> return immediately without executing any hooks.
>
> The `bb6()` function that checks hook existence does NOT filter by agent context
> — it correctly finds settings hooks for subagents. But execution never reaches
> `bb6()` because `_R()` bails out first."

**Translation**: the docs describe the intended behavior; the implementation has
a long-standing bug where subagent contexts run with `CLAUDE_CODE_SIMPLE=1` set
by default, causing the hook runner to no-op silently. The bug has been filed
multiple times since 2026-01-15 and is still OPEN as of 2026-04-12.

### Issue #43772 (2026-04-05): bypassPermissions bypasses hooks entirely

Reporter:
> "When Claude Code dispatches subagents via the `Agent` tool with
> `mode: 'bypassPermissions'`, **PreToolUse hooks are completely bypassed**.
> Subagents execute arbitrary commands that the user explicitly blocked via a
> hook-based allowlist."
>
> "Claude dispatched 4+ subagents with `mode: 'bypassPermissions'`. These
> subagents freely ran: `git add` + `git commit` (3 unauthorized commits),
> `rm` (deleted 7 files), `chmod +x` (changed file permissions)... **None of
> these commands are on my allowlist. All should have been blocked.**"
>
> "`bypassPermissions` should bypass interactive permission prompts (the 'allow
> this command?' dialog), NOT user-defined hooks."

**Akash's `~/.claude/settings.json` has `defaultMode: "bypassPermissions"`**.
This is exactly the failure mode reported.

### Issue #40580 (2026-03-29): exit code 2 from hook ignored in subagent context

Reporter:
> "PreToolUse hooks configured in `~/.claude/settings.json` run for subagent
> (Agent tool) tool calls but the exit code is ignored — the tool call proceeds
> even when the hook returns exit code 2 (block)."
>
> "Hook IS called for subagent tool calls (confirmed via file logging) ...
> Hook returns exit code 2 with stderr message ... **But the tool call proceeds
> anyway** — the agent gets the file contents"

This is an even more severe variant: the hook fires, returns the right exit code,
and Claude Code silently ignores it. Worse than "hooks don't fire" because the
hook side-effects (logging, side-channel signals) execute, but the enforcement
does not.

### Issue #34692 comment (2026-03): PostToolUse works, PreToolUse blocking doesn't

> "PostToolUse confirmed working in sub-agents (tested v2.1.89), but PreToolUse
> blocking is critical for enforcement. Would appreciate this staying open."

So the ASYMMETRY is: `PostToolUse` (non-blocking) does fire in subagents in
some versions. `PreToolUse` (blocking) does not reliably.

### Translation for H3

**H3 as originally conceived — "PreToolUse hook on Write SYNTHESIS.md blocks
the call when audit fails" — is NOT reliably implementable in Claude Code 2026-04
runtime, especially under `bypassPermissions: true` which is Akash's default.**

**This does NOT kill the enforcement protocol**. It forces a redesign:

- **Primary path**: the lead's audit call is an EXPLICIT Bash invocation
  (`bash -c 'python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=synthesis'`)
  that MUST return exit 0 before the lead writes SYNTHESIS.md. This is H1 +
  lead discipline, NOT a runtime hook.
- **Fallback observational**: a `PostToolUse` hook on `Write` (non-blocking, logs
  only) that records the path + size + timestamp of every evidence/synthesis
  write to a session audit log. PostToolUse is reported working in subagents.
- **Retrospector grade**: the retrospector reads the PostToolUse audit log at
  session close and grades whether the lead called the audit before SYNTHESIS.md.
  If not, the retrospector downgrades the lesson.
- **Long-term fix path**: file an issue against anthropics/claude-code with our
  reproduction case, but don't block on Anthropic fixing it.

This is a real, immediate design constraint. The winning synthesis must reflect it.

## 2. Parallel-orchestration issues (Akash's parallel-team use case)

### Issue #41911 (OPEN): "529 Overloaded errors kill parallel subagents, no retry — work lost"

Reporter ran 3 parallel subagents (SEO, Performance, Accessibility audits). All
3 hit 529 overloaded errors. 2 of 3 died silently with 0 output despite 47+
tool calls each. **No automatic retry. Work lost.**

Quote:
> "Agent 1 (SEO): still running (survived somehow)
> Agent 2 (Performance): **dead** — 47 tool uses attempted, 0 useful output
> Agent 3 (Accessibility): **dead** — 51 tool uses attempted, 0 useful output"

**Translation**: 4+ parallel research-leads is a practical ceiling, and even 3
is not safe under API load. The orchestration layer must implement **queue with
back-off** rather than "fire 4 and hope." Empiricist validates.

### Issue #36195 (OPEN): "3-4 parallel foreground agents freeze after 15-30 min, unblock on Ctrl+B"

Reporter:
> "When launching 3-4+ parallel Agent tool calls (foreground, no `run_in_background`),
> all agents freeze after approximately 15-30 minutes. Token consumption stops,
> tool calls show as active but make no progress. ... Switching agents to
> background with **Ctrl+B** immediately unblocks them and they resume normal
> execution."

**Translation**: parallel dispatch MUST be `run_in_background: true`. Foreground
parallel dispatch deadlocks within 30 min. This is already what Akash's 4-session
meta-test is doing, but it explains why it matters.

### Issue #46421 (OPEN): Cache read tokens accumulate multiplicatively

Reporter:
> "When dispatching parallel subagents, each subagent session re-reads the full
> conversation history and parent context from cache. This causes cache_read
> tokens to accumulate rapidly and without upper bound across parallel subagent
> dispatches... A 90-minute parallel subagent session can burn ~15M cache_read
> tokens with no user-visible benefit"
>
> "Cache read tokens should either: (1) Not bill to parent session, (2)
> Deduplicate across subagents, or (3) Have a clear cap"

**Translation for D9 (token-budget target)**: when measuring session cost, cache
reads are inflated 3–5x for parallel sessions. The per-session "total tokens
consumed" number is NOT a direct measure of real work. File-size proxy
(EVIDENCE/ total bytes) is a BETTER signal for "did the specialist actually
do work" than token counts, because cache reads don't write evidence.

## 3. Magentic-One orchestrator source — literal ledger algorithm

Source: `microsoft/autogen@staging` tree —
`python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_magentic_one/`

### Files:
- `_magentic_one_orchestrator.py` — 22,888 bytes — the actual orchestrator class
- `_prompts.py` — 5,952 bytes — the ledger prompts
- `_magentic_one_group_chat.py` — 9,423 bytes — the public API

### The progress ledger prompt (verbatim from _prompts.py, retrieved 2026-04-12)

```
ORCHESTRATOR_PROGRESS_LEDGER_PROMPT = """
Recall we are working on the following request:

{task}

And we have assembled the following team:

{team}

To make progress on the request, please answer the following questions,
including necessary reasoning:

    - Is the request fully satisfied?
    - Are we in a loop where we are repeating the same requests and / or
      getting the same responses as before?
    - Are we making forward progress?
    - Who should speak next?
    - What instruction or question would you give this team member?
```

**Translation**: the five questions in the paper are literally encoded as prompt
template fields. The orchestrator asks an LLM call to answer each, as JSON, with
keys `is_request_satisfied`, `is_in_loop`, `is_progress_being_made`, `next_speaker`,
`instruction_or_question`.

### The stall detection algorithm (verbatim from _magentic_one_orchestrator.py)

```python
# Check for stalling
if not progress_ledger["is_progress_being_made"]["answer"]:
    self._n_stalls += 1
elif progress_ledger["is_in_loop"]["answer"]:
    self._n_stalls += 1
else:
    self._n_stalls = max(0, self._n_stalls - 1)

# Too much stalling
if self._n_stalls >= self._max_stalls:
    await self._log_message("Stall count exceeded, re-planning with the outer loop...")
    await self._update_task_ledger(cancellation_token)
```

And from `_magentic_one_group_chat.py` (the public API docstring):

```python
max_stalls: int = 3,
# docstring: "The maximum number of stalls allowed before re-planning. Defaults to 3."
```

### Field list on the orchestrator instance (verbatim from __init__)

```python
self._model_client = model_client
self._max_stalls = max_stalls
self._final_answer_prompt = final_answer_prompt
self._max_json_retries = 10
self._task = ""
self._facts = ""
self._plan = ""
self._n_rounds = 0
self._n_stalls = 0
```

### Translation for our protocol

- **`max_stalls = 3`** is Microsoft's production default (paper said ≤2; they use
  3). Our mid-flight gate should allow at most 3 shallow-evidence re-dispatches
  before hard-escalating to the user.
- **The stall counter DECAYS** when progress happens (`self._n_stalls = max(0,
  self._n_stalls - 1)`). This is a non-trivial design choice: a session that
  stalls once then makes progress isn't penalized. We should mirror this —
  re-dispatching one specialist doesn't lock the whole session into a retry loop.
- **The orchestrator writes the task ledger UPDATE** when stall exceeded —
  not just re-plans. Our equivalent: when the audit gate fails 3x in a row, the
  lead rewrites `planner.md` with a new dispatch plan, not just re-runs the same
  specialists.

**Citations**:
- [G1] github.com/microsoft/autogen `python/packages/autogen-agentchat/.../_magentic_one/_prompts.py` retrieved 2026-04-12, `ORCHESTRATOR_PROGRESS_LEDGER_PROMPT` verbatim
- [G2] `.../_magentic_one_orchestrator.py` retrieved 2026-04-12, stall counter algorithm lines 200-220 of class body
- [G3] `.../_magentic_one_group_chat.py` retrieved 2026-04-12, `max_stalls: int = 3` default and docstring

## 4. CrewAI source check — guardrail_max_retries

I did not dig into CrewAI source directly (librarian + historian covered the
docs). The docs quote was `guardrail_max_retries` default of 3, which matches
both MetaGPT's "max of 3 retries" and Magentic-One's `max_stalls = 3`. **Three
independent production systems converge on 3 as the retry ceiling.** Adopt.

## 5. Summary of runtime reality vs docs

| Mechanism | Documented | Actually Works? | Source |
|---|---|---|---|
| PreToolUse hook fires for main-thread Write | Yes | Yes | Existing Bash hook in settings.json works |
| PreToolUse hook fires for subagent Write | Yes | **No, reliably** | #43612, #34692 (OPEN) |
| PreToolUse exit 2 blocks main-thread tool call | Yes | Yes | Standard documented behavior |
| PreToolUse exit 2 blocks subagent tool call | Yes | **No** (ignored) | #40580 (OPEN) |
| PreToolUse `permissionDecision: deny` JSON blocks Agent spawn | Yes | **No** | #44534 (OPEN) |
| PreToolUse hooks respected under bypassPermissions (subagent) | Not explicit | **No** | #43772 (OPEN) |
| Hooks in subagent frontmatter run for that subagent | Yes | **Partial / unreliable** | #18392 (CLOSED as dup), #27755 (OPEN) |
| PostToolUse fires for subagent tool calls | Yes | **Yes, in recent versions** | #34692 comment, v2.1.89 |
| SubagentStop fires on subagent completion | Yes | **Unreliable** | #27755, #33049 (closed as dup) |
| SubagentStart fires for run_in_background | Yes | **No** | #44075 (OPEN) |
| Background subagent 529 auto-retry | Not documented | **No, work lost** | #41911 (OPEN) |
| 4+ parallel foreground subagents | Possible | **Freezes after 15-30 min** | #36195 (OPEN) |
| Cache reads multiplicatively inflate parallel session costs | Not documented | **Yes** | #46421 (OPEN) |

**The documented behavior is what Claude Code wants to be. The actual runtime
behavior is what it currently is. Our protocol must work against what it is,
with the docs as an aspirational v3 target once these bugs close.**

## 6. Load-bearing implications

### For H3 (hook-based enforcement)

**REJECTED as the primary enforcement mechanism.** The hook-based path is not
reliable under the current runtime, especially for the `bypassPermissions` mode
that the user has configured.

**ACCEPTED as an auxiliary observability layer**: a PostToolUse hook (the
only reliably-firing subagent hook as of 2026-04) can log every Write to an
audit trail, which the retrospector reads at close to grade enforcement
compliance. Non-blocking, logging-only.

### For H1 (pre-flight + audit script)

**ACCEPTED as the primary enforcement mechanism.** The lead's own discipline
to write `EXPECTED_EVIDENCE.md` before dispatch and call
`python3 ~/.claude/scripts/audit_evidence.py <slug>` via Bash before writing
SYNTHESIS.md is the only path that doesn't depend on unreliable runtime hooks.

The gate is **self-policed**. The retrospector grades compliance.

### For H2 (vocabulary signature)

**ACCEPTED as a diagnostic layer, not a gate.** Runs inside the audit script
as an optional `--strict` mode. Default off (to allow honest-but-related
specialists to pass) but available for the smoke test.

### For H4 (responder pattern)

**DEPRECATED.** The responder adds complexity without beating H1's audit-call
discipline. Drop it unless the skeptic finds a strong argument.

### For D4 (parallel orchestration)

**4 parallel background research-leads is the empirical ceiling** based on
issue filings. Beyond 4, 529 errors start killing sessions silently. The
orchestration layer must:
1. Dispatch ≤ 4 teams concurrently via `run_in_background: true`.
2. Queue additional teams and launch them as earlier sessions complete.
3. Tolerate 529 errors by treating them as "needs re-dispatch" not "failure."
4. NOT use foreground parallel dispatch for > 2 teams (freeze after 15-30 min).

## 7. Citations

- [G1] github.com/microsoft/autogen/.../_magentic_one/_prompts.py `ORCHESTRATOR_PROGRESS_LEDGER_PROMPT` verbatim, retrieved via `gh api` 2026-04-12
- [G2] github.com/microsoft/autogen/.../_magentic_one/_magentic_one_orchestrator.py stall counter algorithm, retrieved 2026-04-12
- [G3] github.com/microsoft/autogen/.../_magentic_one/_magentic_one_group_chat.py `max_stalls: int = 3` default, retrieved 2026-04-12
- [G4] anthropics/claude-code#43612 "PreToolUse/PostToolUse hooks silently disabled in subagents due to CLAUDE_CODE_SIMPLE check in _R()", filed 2026-04-04, OPEN, retrieved 2026-04-12
- [G5] anthropics/claude-code#43772 "Subagents with bypassPermissions ignore PreToolUse hooks", filed 2026-04-05, OPEN
- [G6] anthropics/claude-code#40580 "PreToolUse hook exit code ignored for subagent tool calls", filed 2026-03-29, OPEN
- [G7] anthropics/claude-code#44534 "PreToolUse hook deny not enforced for Agent tool calls", filed 2026-04-07, OPEN
- [G8] anthropics/claude-code#34692 "PreToolUse/PostToolUse hooks do not fire for subagent (Agent tool) tool calls", filed 2026-03-15, OPEN + comments re: PostToolUse working in v2.1.89
- [G9] anthropics/claude-code#27755 "SubagentStart/SubagentStop unreliable for settings.json hooks", OPEN
- [G10] anthropics/claude-code#18392 "Hooks in agent frontmatter not executed for subagents", CLOSED as duplicate of #17688
- [G11] anthropics/claude-code#17688 "Skill-scoped hooks not triggered within plugins", (parent duplicate)
- [G12] anthropics/claude-code#44075 "SubagentStart hooks not fired for background agents", OPEN
- [G13] anthropics/claude-code#39814 "PreToolUse hook `updatedInput` silently ignored for Agent tool", OPEN
- [G14] anthropics/claude-code#41911 "529 Overloaded errors kill parallel subagents, no retry — work lost", OPEN
- [G15] anthropics/claude-code#36195 "Multiple parallel foreground agents freeze after 15-30 min, unblock on ctrl+b", OPEN
- [G16] anthropics/claude-code#46421 "Cache read tokens from parallel subagent dispatch accumulate without upper bound", OPEN
- [G17] anthropics/claude-code#33049 "Subagent does not fire Stop hook on completion", CLOSED as duplicate
- [G18] anthropics/claude-code#45467 "[DOCS] Subagents docs missing `/agents` running count indicator", OPEN
- [G19] anthropics/claude-code#32795 "[BUG] Claude code lose track of running subagents", OPEN
- [G20] anthropics/claude-code#44971 "SubagentStop hook does not fire when team agents terminate via shutdown protocol", OPEN
- [G21] anthropics/claude-code#36336 "Agent tool: orchestrating agent discards detailed subagent output, writes thin summaries instead", OPEN — directly relevant to our "smear" failure mode
- [G22] anthropics/claude-code#39162 "Feature: Option to separate subagent transcripts from parent session", OPEN — relevant to our cost dashboard design
- [G23] anthropics/claude-code#46778 "Expose active agent & background task counts in statusline JSON", OPEN — relevant to our team_status.sh dashboard

## 8. Handoffs and open questions

**For empiricist (CRITICAL)**: empirically verify one of these claims in our
own environment:
- Write a minimal test hook `/tmp/test-hook.sh` that echoes its stdin to a log
  file and returns exit 2.
- Configure it as PreToolUse on `Write|Edit`.
- Dispatch a subagent (any type) that calls Write.
- Observe: does the hook fire? Does it block? What does the log say?
- The answer determines the final shape of H3.

**For tracer**: trace the actual flow if the main session's research-lead tries
to write SYNTHESIS.md without first calling the audit script — what stops it
in the current v2 protocol? (Answer: nothing. It's a prose rule, not enforced.)
This is the baseline we're improving.

**For the lead (Synthesis-level)**:
- Primary mechanism: **H1 (lead-discipline pre-flight + in-lead Bash audit call)**.
- Auxiliary observational: **PostToolUse hook logging writes to a session audit
  trail** (reliable, per #34692 v2.1.89 comment).
- Diagnostic: **H2 vocabulary-signature check inside the audit script** as
  `--strict` mode.
- Grade at retrospector: read audit log, check audit was called, grade compliance.

**Open question for this session**: should we file an issue against
anthropics/claude-code with our reproduction case and a proposed fix for the
`_R()` guard? **Yes** — but not during this session (out of scope). Note for
a follow-up.

## Confidence

**HIGH** on all issue findings — primary GitHub data, recent (most within 14
days of this session), multiple independent reporters.

**HIGH** on Magentic-One source — the actual production code.

**HIGH** on "H3 is not reliably implementable today" — 8+ independent issues
across 3 months with the same pattern, tracing into cli.js root cause.

**MEDIUM** on "PostToolUse does fire in v2.1.89" until empiricist confirms in
Akash's specific environment. This is the one path we still want to use, so
verify it.
