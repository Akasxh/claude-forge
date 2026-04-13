---
specialist: research-skeptic
slug: orchestration-full-activation-v1
started: 2026-04-12T08:00Z
completed: 2026-04-12T08:15Z
tool_calls_count: 3
citations_count: 12
confidence: high
---

# Skeptic — adversarial attack on the winning synthesis

Sub-question (from planner): Red-team the winning composition: "is any of this
actually enforceable within the Claude Code subagent runtime given the specific
failure mode Akash named?" Attack the leading hypothesis and identify unstated
assumptions in the synthesis.

## Method

Read full workspace. Generate competing hypotheses. Identify unstated
assumptions. Attack the winning design at the weakest joints. Apply MAST-
driven adversarial lens (FM-3.3 incorrect verification).

I found **6 attacks** that require mitigation and **4 unstated assumptions**
that must be surfaced before the synthesis claims high confidence.

## ATTACK A1: "Lead-discipline is not enforcement, it's a wish"

**Claim**: the winning synthesis centers on "lead calls `audit_evidence.py`
at the mid-flight and synthesis gates." But the lead is literally the same
process/thread that's prone to smear in the first place. A shortcutting lead
that skips 16 specialists will also skip the audit call. The "enforcement"
is the same entity doing the thing it's supposed to be enforcing against.

**Counter-claim**: the audit call is IN the research-lead persona frontmatter
+ PROTOCOL.md text. A shortcutting lead has to actively ignore both. MEMORY.md
grades compliance, so next session's lead reads about the previous session's
lapse.

**Attack defense**: the persona text is no more binding than the current v2
text ("write to EVIDENCE/<name>.md"), which a shortcutter can already
ignore. We're adding a third layer of the same type of rule. The empirical
test of whether persona rules prevent smear is "do past sessions under v2
already exhibit smear?" — per empiricist the answer is NO (3 sibling
sessions, all 49 files pass schema). v2's prose enforcement is in fact
working for this lead, so v2.1's prose enforcement would also work.

**But**: this argument proves v2 works for a disciplined lead, not that
v2.1 adds meaningful safety for an undisciplined one. It's a null result.

**Resolution**: accept that v2.1 enforcement is **structural scaffolding,
not runtime enforcement**. The scaffolding makes the lead's rule-compliance
easier to verify (retrospector reads `_write_audit.log`, compares timestamps),
but a committed shortcutter still has a path. The retrospector's grade IS
the enforcement delta — a session with missing audit calls gets flagged in
MEMORY.md and future sessions start with stricter defaults. This is social/
procedural enforcement, which is real but delayed.

**Mitigation (adopted)**: add a concrete MEMORY.md lesson template for
retrospector to use when audit is skipped:
> "Previous session <slug> wrote SYNTHESIS.md without first calling
> audit_evidence.py. This is a v2.1 protocol violation. Next session must
> include 'verify audit-before-synthesis' in its pre-flight checklist
> explicitly and double-check via Bash before proceeding."

## ATTACK A2: "The audit script itself is not a runtime-level verification"

**Claim**: the audit script is Python code running as a separate process. The
lead invokes it via Bash. If the Bash call fails (timeout, permission, Python
not found), what happens?

**Counter-claim**: the lead reads the exit code and acts accordingly.

**Attack defense**: the lead's "act accordingly" is another rule-compliance
check. A lead that sees `exit 1` and writes SYNTHESIS.md anyway (via Edit
tool, sidestepping the rule) is not prevented by the audit. Only convinced.

**Mitigation (new)**: add a pre-flight environment check. On the first
Bash call to audit_evidence.py in any session, the lead must verify:
1. `python3 --version` returns 3.11+
2. `~/.claude/scripts/audit_evidence.py` exists and is readable
3. A dry-run call returns exit 0 on a known-good session (the smoke test
   positive path: engineering-team-self-evolve-v1)

These are Bash commands. If any fails, the lead escalates to the user
before starting Round 1.

## ATTACK A3: "The schema thresholds are tuned to 3 sessions"

**Claim** (direct from empiricist §9): "3 sibling sessions is small (n=49
files). Are these 3 representative of the true distribution? The adversary's
concern: selection bias."

**Counter-claim**: this is a real limitation. Thresholds will need ongoing
calibration.

**Attack defense**: in the 3 sessions we have, size variance is high
(9.5K to 26K for lens roles). The 2 KB floor is well below even the 1st
percentile (~9.5K). So the MIN_LENS_BYTES threshold catches only genuine
stubs, not honest-but-brief passes. The H2 count floor (4 sections) is
similarly well below real-session medians (6-14).

Where the calibration IS fragile:
- `MIN_CITATIONS_EXTERNAL_LENS = 3`: empiricist recently expanded the
  regex to include `EVIDENCE/<name>.md` cross-refs and `retrieved YYYY-MM-DD`
  markers. The distribution shifted upward. A more conservative threshold
  would be `≥ 5`, but then some honest-but-brief external-source files
  fail (memory-layer-v1 skeptic had 3 citations in the original regex,
  5 in the new regex — close to threshold either way).
- `T_smear = 0.60`: already flagged MEDIUM by linguist.

**Mitigation (new)**: publish the threshold constants as CLI flags so users
can override per session:
```bash
audit_evidence.py <slug> --min-lens-bytes 3000 --min-h2 5 --min-citations-external 5 --smear-threshold 0.55
```
This lets Akash tune per session type and re-calibrate when real data
arrives. Also: the retrospector should run with default thresholds but
also with `--strict --smear-threshold 0.50` and flag any delta between
the two runs in MEMORY.md.

## ATTACK A4: "PostToolUse hook reliability is assumed on the basis of one comment"

**Claim**: the github-miner cites issue #34692 comment from user `prodan-s`:
"PostToolUse confirmed working in sub-agents (tested v2.1.89)." This is ONE
data point from ONE user on ONE version, extrapolated to our v2.1.101.

**Counter-claim**: it's consistent with other issues (the ones that complain
about PreToolUse failing explicitly note PostToolUse working in some cases).

**Attack defense**: "consistent with other issues" is weak. We did not
actually test PostToolUse hook firing in v2.1.101 in Akash's specific
configuration. Empiricist E_a tested the SCRIPT works on synthetic input
but not that the SCRIPT gets called by the runtime.

**Mitigation (adopted)**: the empiricist handoff already flagged this as a
"live-fire test Akash should run post-session." The synthesis must include
this as a **pre-deployment verification step** (not a design assumption).

Add to the delivered protocol:
> "Before enabling the PostToolUse hook in `settings.json`, run the live-
> fire test: configure the hook, launch a test subagent that writes a file,
> tail the audit log. If a new line appears, PostToolUse works in this
> environment and the auxiliary observational layer is active. If not, drop
> the hook block and run lead-discipline-only."

## ATTACK A5: "The smear simulation was hypothetical; real smear might be different"

**Claim**: tracer §3 described a smear where the lead writes short stubs.
But the real lead-generalist-smear failure mode may look different: a lead
that writes LONG stubs (mechanically filling in the schema with synthetic
content) which would pass the size + H2 + citation checks.

**Counter-claim**: `--strict` mode's Jaccard check catches this.

**Attack defense**: linguist flagged `T_smear = 0.60` as MEDIUM. Real
mechanically-filled stubs might cluster closer to 0.55 or 0.50 depending
on the LLM's lexicon variation.

**Hard attack**: an adversarial synthetic test is required. Create a
synthetic 8-file corpus where the same content is rewritten through 8
different "voices" with different section labels. Measure Jaccard. If
the max pair is < 0.60, our threshold is wrong.

**Mitigation (adopted)**: flag this as Round 3 / smoke-test follow-up.
Create `~/.claude/teams/research/SMOKE_TEST_smear/` with 8 lexically-
similar files and confirm `--strict` catches it. If the Jaccard doesn't
exceed 0.60, tighten to 0.50. Defer to the executor.

## ATTACK A6: "The '4 parallel teams is the ceiling' is based on issue reports, not our own test"

**Claim**: github-miner cites issue #41911 (529 Overloaded kills parallel
subagents at 3+ concurrent) and #36195 (4+ foreground agents freeze at
15-30 min). But these are 3rd-party reports with specific configurations
(Windows 10 in one case). Akash's Linux environment may behave differently.

**Counter-claim**: the live-fire test during this session has 4 background
sessions running concurrently, and 3 have already closed, so empirically
the ceiling is AT LEAST 4 for background mode.

**Attack defense**: 3 of 4 sibling sessions have closed by mid-session.
That's strong evidence. But the closings are sequential (one at a time),
which means the peak concurrent count may have been lower than 4 at any
moment. Also, the 529 errors from #41911 happened during "peak hours" per
the reporter — we haven't tested against peak Anthropic API load.

**Resolution**: the conclusion "4 is the safe ceiling" is correct but
qualified: "4 is safe for NON-PEAK API load; under peak load, 529s may
kill parallel sessions." The orchestration layer should:
1. Try launching 4 background subagents.
2. If any die with 529 within 5 min, re-launch with backoff, reduce
   ceiling to 3 and queue.
3. If more die, reduce further.
This is adaptive, not fixed.

**Mitigation (adopted)**: the launch pattern in the synthesis should not
hard-code N=4. It should use adaptive fallback with 529-detection.

## UNSTATED ASSUMPTIONS surfaced

### UA1: "The lead will write EXPECTED_EVIDENCE.md in Round 0"

This is a new step. Nothing in v2 prepares the lead to write this file.
The v2.1 research-lead persona MUST include an explicit rule. Otherwise
the audit falls back to the team-default roster, which loses per-session
specialization (some sessions should skip archaeologist, some should add
custom specialists like historian-addendum).

**Mitigation**: D7 (research-lead.md persona edits) must include
"Step 1.5: write EXPECTED_EVIDENCE.md based on planner's recommendation"
as a hard rule with specific output format.

### UA2: "The YAML frontmatter v2.1 schema is bought-into by all specialists"

Each of the 17 specialist persona files (`~/.claude/agents/research/*.md`)
currently specifies a deliverable section but NOT a YAML frontmatter. For
v2.1, we need to either:
- (a) Update all 17 persona files to include frontmatter in their deliverable
  template
- (b) Keep the frontmatter optional (backward-compat) — v2-legacy files
  continue passing with "grandfathered" status

Empiricist's audit already supports (b). This is the correct choice because
(a) is a 17-file edit that adds backward-compat risk to the 3 in-flight
sessions. **Adopt option (b)**. Flag a future v2.2 session to migrate the
personas if new sessions consistently use frontmatter.

### UA3: "The retrospector can read `_write_audit.log` at close"

The PostToolUse hook writes to `<workspace>/_write_audit.log`. The
retrospector's method section needs a new step: "read the write audit log,
verify that a Bash invocation of audit_evidence.py appears before the
SYNTHESIS.md write, grade compliance." This is a persona edit for
`research-retrospector.md`.

**Mitigation**: D7 includes both research-lead AND research-retrospector
persona edits.

### UA4: "Users of parallel-team orchestration know to use background: true"

The dispatch pattern in the D4 deliverable uses `Agent(background: true)`.
But the default is `false` per the sub-agents docs. If Akash forgets to
pass `background: true`, he'll hit the 4-agent-foreground-freeze issue
within 30 min. This is a protocol documentation issue.

**Mitigation**: D8 (CLAUDE.md delta) must include an explicit snippet with
`background: true` in the example, and a warning about what happens if it's
omitted.

## Competing hypotheses I want documented

For the retrospector to carry forward:

**CH1**: the design should eventually migrate to a **main-thread research-lead**
invocation pattern (`claude --agent research-lead`) because main-thread hooks
DO work reliably. This is blocked today by the adopted-persona default being
more convenient. Future retrospector may flag a pain point that justifies
the migration.

**CH2**: the design should add a **session-wide `EXPECTED_EVIDENCE.lock`**
file that gets written with a hash of the contract, and the final SYNTHESIS
must include the hash in its frontmatter. This is cryptographic integrity
("the synthesis was made against THIS contract"). Overkill for today; may
become necessary if multi-session handoffs get more formal.

**CH3**: the design should integrate with **MEMORY.md** so that the
retrospector's compliance grade becomes a persistent score that the lead
reads at the START of the next session. The planner then uses that score to
tune dispatch aggressiveness. This IS in the mitigation for A1 — the lesson
template.

## Conclusion

The winning synthesis is defensible but requires the 6 mitigations and 4
assumption-surfacings above. With those, I withdraw objections and grade
the design **ready for Round 3 evaluator**.

The PRIMARY enforcement is lead-discipline, structurally scaffolded by
the audit script. This is weaker than "runtime-level hook block" but
stronger than "prose rule in PROTOCOL.md." It sits between the two and
depends on retrospector-as-social-enforcement for the closing-the-loop step.

**Explicit confidence on each claim**:
- **High**: pattern is implementable today with stdlib Python and existing
  Bash primitives
- **High**: catches deliberate short-stub smear (empirically validated)
- **Medium**: catches committed synthetic-content smear (requires smoke test)
- **High**: backward-compatible with all 3 sibling sessions
- **Medium**: retrospector-as-social-enforcement is real (depends on
  MEMORY.md being read at session start, which is currently true)
- **High**: parallel orchestration ceiling is ≥ 4 background concurrent
  teams (observed live)
- **Medium**: ceiling holds under peak API load (not tested)

## Citations

- [SK1] synthesist.md §C1 (contradiction framing)
- [SK2] moderator.md §Verdict (reframe + complementarity)
- [SK3] github-miner.md §1 (issues #43612/#43772/#40580 as runtime ground truth)
- [SK4] empiricist.md §5 (smoke test with deliberate shortcut)
- [SK5] empiricist.md §7 (token-budget target)
- [SK6] linguist.md §2 (T_smear = 0.60 MEDIUM calibration)
- [SK7] tracer.md §3 (smear simulation under v2.1)
- [SK8] tracer.md §5 (residual risks R1-R5)
- [SK9] historian.md §2 (Magentic-One max_stalls=3)
- [SK10] web-miner.md §2 (agents-observe limitations)
- [SK11] `~/.claude/agents/research/research-lead.md` v2 current workflow rules
- [SK12] `~/.claude/agent-memory/research-lead/MEMORY.md` lessons 1-13 as the
  social-enforcement substrate

## Handoff to adversary

Adversary should audit the SOURCES cited by this synthesis for corpus-level
problems:
- The github-miner's issue pile is first-party GitHub data but the issues
  are reported by third parties. Are any of them astroturf / SEO / gaming?
- The Magentic-One source code is MICROSOFT's published repo. HIGH-PRIMARY.
- The Anthropic docs are PRIMARY but documented-vs-actual gap is known.
  REPORTED-NOT-VERIFIED on the subagent hook claims specifically.
- The HN 2026 ecosystem (web-miner §2) is MIXED — top hits (agents-observe
  76/28) are legitimate; single-digit posts are MIXED / noise.

## Confidence

**HIGH** on the 6 attacks being substantive and requiring mitigation.
**HIGH** on the 4 unstated assumptions being real and surfacing-worthy.
**MEDIUM** on whether ALL attacks are addressed — A5 (smear simulation)
requires a follow-up synthetic test that's out of scope for this session.
**HIGH** on the winning synthesis being defensible after mitigations.
