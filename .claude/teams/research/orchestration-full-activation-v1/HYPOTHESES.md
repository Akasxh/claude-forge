# HYPOTHESES — orchestration-full-activation-v1

Seeded by research-lead BEFORE dispatch per v2 protocol Round 0 rule.
These are the competing enforcement strategies the wide opener will test.
The skeptic and moderator will attack these in Round 2.

Four candidates for the core enforcement mechanism. Each has a different
cost/strictness/implementability profile; the wide opener will probe which
is implementable *today* inside the Claude Code subagent runtime AND
*effective* at catching lead-generalist-smear.

## H1 — Pre-flight checklist (contract-before-dispatch)

**Design**: Before the lead dispatches Round 1, it writes a machine-readable
`EXPECTED_EVIDENCE.md` (or `.json`) listing every specialist file that MUST
exist by session close, with per-specialist deadlines and required sections.
The lead reads this file at every gate to know what must be present. No
runtime hook — the lead self-polices. The audit script (post-session, and
mid-session callable) reads EXPECTED_EVIDENCE.md and the EVIDENCE/ directory,
returning PASS/FAIL with specific missing/shallow entries.

**How it catches the failure**: lead cannot smear 16 lens passes into 1
because it committed in writing to producing 17 distinct files with
specific sections. The mid-flight audit (called at the Round 1 → Round 2
boundary) fails hard if any evidence file is missing or shallow.

**Pros**:
- Implementable today with stdlib Python. No Claude Code hook needed.
- Runs identically in both main-thread and adopted-persona mode.
- Enforces the "contract" metaphor exactly: the file is the promise.
- Easy to extend per team (engineering has different specialists).
- Easy for the retrospector to grade ("did each specialist's file hit its schema?").

**Cons**:
- The lead can still write the file itself, regardless of whether a subagent
  actually ran. A smeared lead could fake 17 schema-passing files from a
  single generalist pass.
- Schema enforcement is a weak proxy for "distinct lens actually ran."
  A committed shortcutter can satisfy the schema mechanically.
- Requires discipline: the lead has to write EXPECTED_EVIDENCE.md before
  dispatch, read it at gate time, and trust the audit. If the lead skips
  the pre-flight, the whole mechanism collapses.
- Mid-flight audit adds one Bash call per gate. Tool-call budget cost.

**Predicted by**: GNU Make / Bazel target-as-contract pattern, all
artifact-based CI systems, SWE-bench's test-as-contract evaluation model.
Hypothesis is this is **necessary but not sufficient**.

## H2 — Per-specialist token attribution ("receipts before synthesis")

**Design**: Every specialist's evidence file must include a YAML frontmatter
block recording `started`, `completed`, `tool_calls_count`, `distinct_citations`,
and a `method_signature` (a unique hash over the specialist's method vocabulary).
The audit script verifies that the signatures across 17 files are
approximately distinct (Jaccard similarity across pairs < some threshold)
and that the total token proxy (file-size sum) exceeds the minimum
per-specialist budget × 17. If 17 files have similar vocabulary signatures,
the audit flags it as "lead-generalist-smear detected" and fails the gate.

**How it catches the failure**: even if a committed shortcutter writes 17
schema-passing files, the vocabulary-signature check reveals that all 17
came from the same token distribution — because they did, they were one
lens pass. The audit cannot be fooled by mechanical schema satisfaction;
it measures lexical diversity.

**Pros**:
- Defeats mechanical schema-fakes that would pass H1.
- Adds a statistical lens-distinctness metric, not just structural.
- Natural fit for post-session retrospection: "how distinct were the
  specialists' contributions statistically?"
- Provides real cost-dashboard data via frontmatter counts.

**Cons**:
- Signature computation is non-trivial to get right. False positives
  on honest-but-related specialists (historian and librarian naturally
  share vocabulary). False negatives on a sophisticated shortcutter
  who injects synthetic vocabulary.
- Token attribution via file size is a proxy, not ground truth. A
  verbose shortcutter can inflate file size without running the lens.
- Still doesn't verify the specialist actually ran; only that the
  output is lexically distinct.

**Predicted by**: MAST paper's failure-mode analysis plus classical
plagiarism detection (Jaccard / MinHash). Hypothesis is this is
**diagnostic, not preventive** — catches smear after the fact.

## H3 — Hook-based runtime enforcement

**Design**: Add a Claude Code `PreToolUse` hook on `Write` that, when the
target path matches `**/SYNTHESIS.md`, checks the sibling `EVIDENCE/`
directory against the session's `EXPECTED_EVIDENCE.md` contract. If any
expected file is missing or fails the schema check, the hook blocks the
Write with a structured error. The lead cannot write SYNTHESIS.md until
every specialist evidence file exists and passes schema. No post-hoc
audit — enforcement is at write-time.

**How it catches the failure**: the runtime physically refuses to let
the lead write SYNTHESIS.md until the contract is satisfied. A shortcutter
who tries to skip specialists hits a hard runtime block and must go back
and produce the missing evidence.

**Pros**:
- Strongest enforcement: the gate cannot be forgotten or skipped
  because the runtime enforces it at tool-call time.
- Self-documenting: the block message tells the lead exactly what's missing.
- Zero lead discipline required: works even if the lead tries to
  short-circuit.

**Cons**:
- Requires Claude Code hooks to be reliable and testable. Need to verify
  PreToolUse hooks actually fire on subagent Write calls, not just main
  thread.
- Hook is a shell script executing Python; adds latency to every Write.
- Debugging is harder when the hook silently blocks.
- If the hook has a bug, it can block legitimate writes too.
- May not work if the subagent context is sandboxed from the main
  session's hook config.

**Predicted by**: Claude Code settings.json hooks documentation, CI
pre-commit hook pattern, Linux LSM-style reference monitors. Hypothesis
is this is **most effective if implementable** — we need to verify the
hook actually runs for subagent tool calls, which is a technical unknown.

## H4 — Schema-enforced evidence files via "responder pattern"

**Design**: Instead of the lead writing evidence files inline in adopted-persona
mode, each specialist's method ends with an explicit Bash call to a helper
script `evidence_responder.sh <specialist-name> <slug>` that the specialist
must call before returning. The responder script opens a fresh file
`EVIDENCE/<name>.md`, writes the YAML frontmatter, and then the specialist
fills in the body with a subsequent Edit call. The responder pattern makes
each evidence file creation an explicit, traceable, timestamped event.
Combined with H1's pre-flight contract, the lead can only create
`EVIDENCE/<name>.md` by invoking the specialist's contract via the responder.

**How it catches the failure**: the responder script is the only legitimate
path to create an evidence file. Each invocation is logged with a timestamp.
The audit script checks that N responder invocations happened (via a
session-scoped log the responder writes) and that each has a completed
body. Smear is caught because the lead would have to invoke the responder
17 times with 17 distinct `<specialist-name>` arguments AND produce 17
distinct body contents, which is strictly harder than writing 17 files
directly in a single thinking stretch.

**Pros**:
- Every evidence file creation is a timestamped event, enabling real
  per-specialist latency measurement (gap between responder call and
  body completion = specialist's actual work time).
- The responder can enforce schema at creation time, rejecting short
  frontmatter immediately.
- Works identically in both main-thread and adopted-persona mode.
- Script is stdlib bash, no hook dependency.

**Cons**:
- Adds 1 bash call per specialist = 17 extra tool calls per session.
  Tool-call efficiency hit, though small.
- Requires the lead to remember to invoke the responder before each
  specialist body write. One more rule to follow.
- Adds a subtle layer of indirection that may confuse debugging.

**Predicted by**: Unix file-locking / PID file patterns, the GNU Make
`touch` idiom, database transaction prepare/commit, Kubernetes admission
controllers. Hypothesis is this is **implementable today without runtime
changes and catches more than H1 alone**.

## The meta-hypothesis

The winning strategy is **not one of the four alone**, but a **compositional
defense**:

- **H1** is the baseline contract (pre-flight + schema + mid-flight audit).
- **H4** adds timestamped creation events that let us measure latency.
- **H2**'s vocabulary-signature check is the final diagnostic layer that
  catches a committed shortcutter who mechanically satisfies H1+H4.
- **H3** is the ideal runtime enforcement layer but is gated on verifying
  Claude Code hooks fire for subagent tool calls. If they do, adopt it.
  If they don't, fall back to H1+H4+H2.

The wide opener must determine:
1. Which of H1/H2/H4 is strictly implementable today with stdlib tools.
2. Whether H3 is implementable — librarian investigates Claude Code hook
   semantics, empiricist runs a smoke test.
3. Whether the composition above is coherent or over-engineered.
4. Whether there's a **fifth option** the literature suggests that none
   of these capture (historian's job).

## Secondary hypotheses on parallel orchestration

### PH1 — Filesystem polling is the only safe observability channel

Main session can poll (a) `ls EVIDENCE/` counts and mtimes, (b) `LOG.md`
tail via `wc -l`, (c) `SYNTHESIS.md` existence. It should NOT read
`.output` JSONL streams (they grow unboundedly). Should NOT read full
evidence files mid-session (may be in-progress). Polling frequency should
be "on-demand when user asks" not "every N seconds" because the main
session has no background loop.

### PH2 — Background agents don't share state; reconciliation is file-based

`Agent(run_in_background=true)` spawns a sibling session that writes to
its own workspace. Main session reads the workspace when the agent
completes (via completion notification) or when asked. Memory-layer
merging happens at close via the lock protocol (engineering-team session
designs it). Context isolation is complete; there is no shared RAM.

### PH3 — Rate limiting: 4 concurrent research-leads is the practical ceiling

Anthropic Max plan has rate limits in the low-thousands tokens/min range
per account. A fully-active research session with 17 specialists running
real tool calls is probably in the 200-500 KTok range. 4 concurrent
sessions at that rate saturates the rate limit; 8 probably throttles.
The main session should dispatch ≤ 4 background teams at once and queue
the rest. Empiricist validates this.

### PH4 — The cost dashboard must be stateless

A polling script `team_status.sh` should be idempotent, fast (< 1 second),
and derive everything from filesystem state (file sizes, mtimes, existence).
No database, no daemon, no state file. Runs on-demand, prints a table,
exits.
