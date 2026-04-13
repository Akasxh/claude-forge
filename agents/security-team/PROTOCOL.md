# Security & Review Team Protocol v1

The Security & Review Team is the independent auditor in this setup. It
catches what the Engineering Team's internal reviewer misses: OWASP
vulnerabilities, dependency CVEs, secrets in code, architectural flaws,
threat model gaps, license compliance violations, and infrastructure
misconfigurations. It operates on ANY codebase, detecting language,
framework, and dependency manager automatically.

This is a **leader + 13 specialists** hierarchy, **all running on
Opus with `effort: max`** (hard contract, no downgrades ever),
coordinating through **files on disk**.

This document is the contract every team member reads before acting.

## Scope model (v1)

**Global (~/.claude/) -- shared across all projects:**
- `~/.claude/teams/security/PROTOCOL.md` -- this document
- `~/.claude/agents/security/*.md` -- all 14 agent personas
- `~/.claude/agent-memory/security-lead/` -- institutional memory (cross-project)
- `~/.claude/scripts/` -- audit_evidence.py, team_status.sh (shared with Research/Engineering)

**Per-project (<cwd>/.claude/) -- isolated per project directory:**
- `.claude/teams/security/INDEX.md` -- session index for THIS project only
- `.claude/teams/security/<slug>/` -- all session artifacts

## What this team does

Engineering Team ships code. Security Team audits it independently and
issues a verdict: BLOCKER, ADVISORY, or PASS. The two teams connect
via the cross-team handoff protocol (Section: Cross-team handoff).

Security Team v1 is designed for **audit tasks** -- reviewing,
scanning, and analyzing code for security issues -- not for fixing them.
Findings include remediation guidance, but the Engineering Team or the
developer implements fixes.

## Design principles

### Hybrid pipeline (SAST tools + LLM reasoning + self-verification)

Raw LLM vulnerability scanning has ~86% false positive rate (Semgrep/Anthropic
study, 2025). LLM post-filtering of SAST results reduces FPR from >90% to
<10% (Datadog study, direction validated by IRIS neuro-symbolic approach).

Every security specialist follows a **3-phase method**:
1. **Tool phase**: run the relevant automated tool (if available on the system)
2. **Reasoning phase**: LLM analysis of tool output + independent scan for
   novel patterns that tools miss (business logic flaws, auth bypasses,
   cross-component data flow issues)
3. **Verification phase**: re-examine each finding, attempt to disprove it,
   assign confidence rating. Only findings that survive verification are reported.

This pipeline is non-negotiable. A specialist that skips the verification
phase is producing noise, not signal.

### Project-agnostic auto-detection

The team works on any codebase without configuration. Auto-detection runs
at session start (Round 0) using this cascade:

```
Step 1: Lock/manifest file detection (most reliable)
  package-lock.json | yarn.lock | pnpm-lock.yaml       -> npm/Node.js
  Cargo.lock | Cargo.toml                                -> Rust
  poetry.lock | requirements.txt | pyproject.toml |
    setup.py | Pipfile                                   -> Python
  go.sum | go.mod                                        -> Go
  Gemfile.lock | Gemfile                                 -> Ruby
  pom.xml | build.gradle | build.gradle.kts              -> Java/Kotlin
  composer.lock | composer.json                          -> PHP
  *.csproj | *.sln                                       -> .NET
  Package.swift                                          -> Swift
  mix.lock                                               -> Elixir

Step 2: Framework markers
  next.config.* -> Next.js    nuxt.config.* -> Nuxt
  angular.json -> Angular     django/ | manage.py -> Django
  config/routes.rb -> Rails   Rocket.toml -> Rust web
  cmd/main.go -> Go CLI

Step 3: Config file signals
  tsconfig.json -> TypeScript  .eslintrc* | biome.json -> JS
  ruff.toml -> Python          rustfmt.toml -> Rust

Step 4: File extension survey
  find . -maxdepth 3 -name "*.py" -o -name "*.js" ... | head -20

Step 5: GitHub linguist fallback (if git remote exists)
  gh api repos/{owner}/{repo}/languages
```

### Tool availability check

After detecting the stack, check what security tools are available:
```bash
command -v semgrep && echo "semgrep"
command -v bandit && echo "bandit"
command -v gitleaks && echo "gitleaks"
command -v npm && echo "npm"
command -v pip-audit && echo "pip-audit"
command -v cargo && echo "cargo"  # for cargo audit
command -v go && echo "go"        # for govulncheck
```

If tools are unavailable, specialists fall back to LLM-only analysis
(Grep-based pattern scanning for secrets, Read-based OWASP checking).
This is slower and has higher false positive rates but works everywhere.
The SECURITY_REPORT.md must note which tools were available vs. unavailable.

### Tool selection per detected stack

| Stack | SAST | SCA | Secrets |
|---|---|---|---|
| JavaScript/TypeScript | Semgrep | npm audit | Gitleaks (or Grep fallback) |
| Python | Semgrep + Bandit | pip-audit | Gitleaks (or Grep fallback) |
| Rust | cargo clippy (sec lints) | cargo audit | Gitleaks (or Grep fallback) |
| Go | Semgrep | govulncheck | Gitleaks (or Grep fallback) |
| Java/Kotlin | CodeQL or Semgrep | OWASP dependency-check | Gitleaks (or Grep fallback) |
| Ruby | Semgrep or Brakeman | bundler-audit | Gitleaks (or Grep fallback) |
| C/C++ | CodeQL | N/A | Gitleaks (or Grep fallback) |
| PHP | Semgrep | composer audit | Gitleaks (or Grep fallback) |
| .NET | CodeQL | dotnet list vulnerabilities | Gitleaks (or Grep fallback) |
| Any | Gitleaks cross-language | Dependabot (if GitHub) | Gitleaks |

## Roster (13 specialists + 1 lead)

| Role | Agent name | Domain | Primary MAST failure | Phase |
|---|---|---|---|---|
| Leader | `security-lead` | orchestration | FM-1.1, FM-1.5, FM-2.2 | all |
| Planner | `security-planner` | dispatch calibration | FM-1.1 | Round 0 |
| OWASP Scanner | `security-owasp-scanner` | Application security (OWASP Top 10) | FM-3.2 | Round 1 |
| Secrets Hunter | `security-secrets-hunter` | Secrets in code + git history | FM-3.2 | Round 1 |
| Dependency Auditor | `security-dependency-auditor` | CVEs, supply chain risk | FM-3.2 | Round 1 |
| Crypto Reviewer | `security-crypto-reviewer` | Cryptographic + data protection | FM-1.2 | Round 1 |
| Architecture Reviewer | `security-architecture-reviewer` | Design-level security | FM-1.2 | Round 1 (full audits) |
| Threat Modeler | `security-threat-modeler` | Attack surface, STRIDE/ASTRIDE | FM-1.1 | Round 1 (full audits) |
| License Auditor | `security-license-auditor` | License compatibility, SBOM | FM-3.2 | Round 1 (compliance audits) |
| Config Scanner | `security-config-scanner` | IaC, security config, CI/CD | FM-3.2 | Round 1 |
| Skeptic | `security-skeptic` | Internal red team of findings | FM-3.3 | Round 2 |
| Evaluator | `security-evaluator` | Quality gate on report | FM-3.1, FM-3.2 | Round 3 |
| Retrospector | `security-retrospector` | Cross-session learning | cross-session | Close |
| Scribe | `security-scribe` | Ledger, MEMORY.md merge | FM-1.4, FM-2.1 | Close |

## Model contract (non-negotiable)

Every agent runs on `opus` with `effort: max`.
Enforced at the frontmatter level. If you see an agent file in
`~/.claude/agents/security/` without these two fields, it is a bug.

## Execution model

Claude Code subagents cannot spawn other subagents. Two valid modes:

1. **Main-thread invocation** (`claude --agent security-lead`): the lead
   dispatches specialists via the `Agent` tool.
2. **Adopted persona** (default when invoked via Agent from another session):
   the lead reads each specialist's persona as a behavioral contract and
   executes its method directly.

## Tier classification (binding)

Every audit is classified before work begins:

- **Quick scan**: Single PR or small diff. Dispatch: owasp-scanner +
  secrets-hunter + dependency-auditor (3 specialists). No architecture,
  no threat model, no license. Target: <5 minutes.
- **Standard audit**: New feature, module, or significant change.
  Dispatch: owasp-scanner + secrets-hunter + dependency-auditor +
  crypto-reviewer + config-scanner (5 specialists). Target: <15 minutes.
- **Full audit**: New repository, major refactor, or compliance review.
  Dispatch: all 8 domain specialists. Target: <30 minutes.
- **Compliance audit**: Full audit + license-auditor emphasis. All 8
  domain specialists with license-auditor running at full depth.

Default bias: when in doubt, pick the higher tier.

## Round structure (v1)

| Round | Name | Output |
|---|---|---|
| Round 0 | Intake + auto-detect | AUDIT_CHARTER.md, detected stack, tier decision |
| Round 1 | Domain specialists | EVIDENCE/<specialist>.md per dispatched specialist |
| Round 2 | Skeptic gate | EVIDENCE/skeptic.md (attacks findings) |
| Round 3 | Evaluator gate | EVIDENCE/evaluator.md, SECURITY_REPORT.md |
| Close | Retrospection + scribe | MEMORY.md updated, INDEX.md entry |

### Round 0 -- Intake + Auto-detect

1. Lead reads `~/.claude/agent-memory/security-lead/MEMORY.md` (first 200 lines).
2. Lead determines audit trigger (engineering handback, user request, or CI).
3. Lead runs auto-detection cascade on target codebase.
4. Lead runs tool availability check.
5. Lead classifies tier (quick/standard/full/compliance).
6. Lead dispatches `security-planner` for dispatch calibration.
7. Lead writes AUDIT_CHARTER.md with: scope, detected stack, available tools,
   tier, specialists to dispatch.

### Round 1 -- Domain specialists (parallel)

Dispatch all tier-appropriate specialists in a single message. Each
specialist follows the 3-phase method (tool -> reason -> verify).

Each specialist writes `EVIDENCE/<name>.md` containing:
- Findings (each with severity, category, file:line, description, remediation)
- Tool output (raw, when a tool was used)
- Verification notes (which findings survived self-verification)
- Confidence assessment

### Round 2 -- Skeptic gate (mandatory for standard+ tiers)

`security-skeptic` reads ALL specialist evidence files and attacks:
1. Are any findings false positives? (Check if conditions for exploitation exist)
2. Are any findings duplicated across specialists? (Deduplicate)
3. Are severity ratings calibrated? (A LOW labeled as HIGH, or vice versa)
4. Are there obvious gaps? (Common vulnerability patterns not checked)

Skeptic writes `EVIDENCE/skeptic.md` with:
- Findings to DOWNGRADE (with reason)
- Findings to UPGRADE (with reason)
- Findings to REMOVE as false positives (with reason)
- Gaps to flag as OPEN_QUESTIONS

### Round 3 -- Evaluator gate + Report

1. Lead integrates all findings (post-skeptic) into SECURITY_REPORT.md.
2. `security-evaluator` grades the report on 5 dimensions:
   - **Coverage**: Were all tier-appropriate domains audited?
   - **Accuracy**: Are findings correctly classified?
   - **Actionability**: Does each finding have a remediation path?
   - **False positive rate**: How many findings survived skeptic review?
   - **Completeness**: Are any obvious attack vectors missing?
3. PASS -> session close.
4. FAIL -> return to Round 1 for targeted re-scan. Hard cap: 2 evaluator re-runs.

### Session close

1. Lead computes session verdict: BLOCKER / ADVISORY / PASS (see thresholds below).
2. `security-retrospector` extracts lessons to staging.
3. `security-scribe` normalizes files, writes INDEX.md entry, runs MEMORY.md merge.
4. If triggered by engineering handback: write SECURITY_VERDICT file to
   engineering workspace.

## Verdict system

### Per-finding severity (CVSS-aligned)

| Severity | Definition | SLA |
|---|---|---|
| CRITICAL | Exploitable with severe impact: RCE, data breach, credential theft, auth bypass allowing admin access | 24 hours |
| HIGH | Exploitable under specific conditions with serious impact | 1 week |
| MEDIUM | Security weakness with limited impact or difficult exploitation | 1 month |
| LOW | Best practice violation, minor concern, informational | Backlog |

### Session verdict (3-tier decision gate)

```
BLOCKER:
  any(finding.severity == CRITICAL) OR
  count(finding.severity == HIGH) >= 3

ADVISORY:
  any(finding.severity in {HIGH, MEDIUM}) AND NOT BLOCKER

PASS:
  all findings are LOW or no findings
```

| Verdict | Engineering action |
|---|---|
| BLOCKER | Must remediate before merge. Engineering session reopened or new session. |
| ADVISORY | Should remediate. Merge allowed with documented risk acceptance. |
| PASS | Clean to merge. |

## Cross-team handoff protocol

### Forward path: Engineering -> Security

**Mode 1: Post-engineering gate (default)**
```
Engineering evaluator PASS
  -> Main session dispatches security-lead with:
     - source: "engineering-handback"
     - scope: "diff" (engineering session's changes)
     - engineering_workspace: <path>
     - target_path: <codebase path>
```

**Mode 2: User-initiated**
```
User: "run security audit on this repo"
  -> Main session dispatches security-lead with:
     - source: "user-request"
     - scope: "full-repo"
     - target_path: <codebase path>
```

### Back path: Security -> Engineering

Security writes its verdict to the engineering workspace:
`<cwd>/.claude/teams/engineering/<eng-slug>/SECURITY_VERDICT_<sec-slug>.md`

Format:
```markdown
# SECURITY VERDICT -- <security-slug>

## Verdict: BLOCKER | ADVISORY | PASS

## Summary
- Critical: N findings
- High: N findings
- Medium: N findings
- Low: N findings

## BLOCKER findings (if any)
[condensed finding descriptions with file:line locations]

## Remediation priority
1. [most critical finding]
2. ...

## Full report
<cwd>/.claude/teams/security/<sec-slug>/SECURITY_REPORT.md
```

### Re-audit after remediation

When engineering addresses BLOCKER findings and requests re-audit:
1. Security receives the engineering diff (changes since last audit)
2. Security re-audits ONLY the remediated areas + regression check
3. Unchanged code is NOT re-scanned (cached baseline)
4. Verdict is computed fresh on all remaining findings

## Shared workspace

```
<cwd>/.claude/teams/security/<slug>/
  AUDIT_CHARTER.md          # lead (Round 0)
  EVIDENCE/
    planner.md              # security-planner
    owasp-scanner.md        # security-owasp-scanner
    secrets-hunter.md       # security-secrets-hunter
    dependency-auditor.md   # security-dependency-auditor
    crypto-reviewer.md      # security-crypto-reviewer
    architecture-reviewer.md # security-architecture-reviewer
    threat-modeler.md       # security-threat-modeler
    license-auditor.md      # security-license-auditor
    config-scanner.md       # security-config-scanner
    skeptic.md              # security-skeptic
    evaluator.md            # security-evaluator
    retrospector.md         # security-retrospector
    scribe.md               # security-scribe
  SECURITY_REPORT.md        # lead (Round 3)
  LOG.md                    # everyone (append-only)
  OPEN_QUESTIONS.md         # lead + any specialist
```

Team-wide files:
```
<cwd>/.claude/teams/security/INDEX.md
~/.claude/agent-memory/security-lead/MEMORY.md
~/.claude/agent-memory/security-lead/staging/
```

## Ownership rules

| File | Writer | Reader |
|---|---|---|
| AUDIT_CHARTER.md | security-lead | everyone |
| EVIDENCE/<name>.md | named specialist only | everyone |
| SECURITY_REPORT.md | security-lead | everyone + engineering |
| LOG.md | everyone (append-only) | everyone |
| INDEX.md | security-scribe only | everyone |
| MEMORY.md | security-retrospector (via staging) + security-scribe (merge) | security-lead at session start |

## Finding schema (mandatory for all domain specialists)

Each finding MUST contain:
```markdown
### [Finding title]
- **Severity**: CRITICAL | HIGH | MEDIUM | LOW
- **Category**: [OWASP category or domain category]
- **Location**: `file.ext:line`
- **Exploitability**: Remote|Local, Authenticated|Unauthenticated
- **Blast radius**: [what an attacker gains]
- **Confidence**: HIGH | MEDIUM | LOW
- **Description**: [what the vulnerability is]
- **Evidence**: [code snippet or tool output]
- **Remediation**:
  ```language
  // VULNERABLE
  [vulnerable code]
  // FIXED
  [fixed code]
  ```
- **Verification notes**: [how this finding was verified / why it's not a false positive]
```

## Parallel-instance memory segregation

Same pattern as Engineering Team:
- Retrospector writes to `staging/<slug>.md`
- Scribe merges via flock + timeout + atomic rename
- Readers never take the lock

## SECURITY_REPORT.md structure

```markdown
# Security Audit Report

## Metadata
- **Scope**: [files/components/repository]
- **Detected stack**: [languages, frameworks, dependency managers]
- **Tools available**: [list]
- **Tools unavailable**: [list]
- **Tier**: quick | standard | full | compliance
- **Trigger**: engineering-handback | user-request

## Verdict: BLOCKER | ADVISORY | PASS

## Summary
| Severity | Count |
|---|---|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |

## Critical Findings (fix immediately)
[findings sorted by severity x exploitability]

## High Findings (fix within 1 week)
[findings]

## Medium Findings (fix within 1 month)
[findings]

## Low Findings (backlog)
[findings]

## Dependency Audit
[SCA results]

## Secrets Scan
[secrets results]

## Architecture Notes (full audits only)
[architecture review]

## Threat Model (full audits only)
[threat model]

## License Compliance (compliance audits only)
[license results]

## Recommendations
[prioritized action items]

## Skeptic notes
[any caveats, false positive risks, gaps]
```

## Escalation

If the evaluator FAILs twice:
1. Deliver PROVISIONAL report with documented gaps
2. Publish OPEN_QUESTIONS.md
3. Dispatch retrospector
4. Notify user that audit is incomplete

## Session naming

`<slug>` chosen by security-lead from the audit target. Examples:
- `vllm-pr-1234-quick`
- `claude-infra-full-audit`
- `webapp-dependency-update`

## Prior art this protocol imports

- **Anthropic Claude Code Security** -- multi-stage verification, reasoning-based analysis
- **OWASP Top 10 (2025)** + **OWASP Top 10 for Agentic Applications (2026)** -- vulnerability taxonomy
- **IRIS** (arxiv 2405.17238) -- neuro-symbolic hybrid (SAST + LLM)
- **ASTRIDE** (arxiv 2512.04785) -- agentic AI threat modeling
- **MITRE ATLAS v5.1** -- AI threat framework
- **Semgrep/Anthropic study** (2025) -- LLM FPR baseline (86% raw, <10% with pipeline)
- **GRASP** -- structured LLM reasoning via DAG over secure coding practices
- **Research Team PROTOCOL v2** -- adversarial gates, MEMORY.md patterns
- **Engineering Team PROTOCOL v1** -- cross-team handoff, staging protocol
- **MAST** (Cemri et al., arxiv 2503.13657) -- failure mode taxonomy
