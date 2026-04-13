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

## Scope model (v1)

**Global (~/.claude/) -- shared across all projects:**
- `~/.claude/teams/security/PROTOCOL.md` -- this document
- `~/.claude/agents/security/*.md` -- all 14 agent personas
- `~/.claude/agent-memory/security-lead/` -- institutional memory

**Per-project (<cwd>/.claude/) -- isolated per project directory:**
- `.claude/teams/security/INDEX.md` -- session index for THIS project only
- `.claude/teams/security/<slug>/` -- all session artifacts

## Design principles

### Hybrid pipeline (SAST tools + LLM reasoning + self-verification)

Raw LLM vulnerability scanning has ~86% false positive rate (Semgrep/Anthropic
study, 2025). LLM post-filtering reduces FPR from >90% to <10% (Datadog study).

Every security specialist follows a **3-phase method**:
1. **Tool phase**: run the relevant automated tool (if available)
2. **Reasoning phase**: LLM analysis + independent scan for novel patterns
3. **Verification phase**: re-examine each finding, attempt to disprove it, assign confidence. Only MEDIUM+ confidence findings are reported.

## Roster (13 specialists + 1 lead)

| Role | Agent name | Domain | Phase |
|---|---|---|---|
| Leader | `security-lead` | orchestration | all |
| Planner | `security-planner` | dispatch calibration | Round 0 |
| OWASP Scanner | `security-owasp-scanner` | OWASP Top 10 (2025) | Round 1 |
| Secrets Hunter | `security-secrets-hunter` | Secrets in code + git history | Round 1 |
| Dependency Auditor | `security-dependency-auditor` | CVEs, supply chain risk | Round 1 |
| Crypto Reviewer | `security-crypto-reviewer` | Cryptographic + data protection | Round 1 |
| Config Scanner | `security-config-scanner` | IaC, security config, CI/CD | Round 1 |
| Architecture Reviewer | `security-architecture-reviewer` | Design-level security | Round 1 (full only) |
| Threat Modeler | `security-threat-modeler` | STRIDE/ASTRIDE | Round 1 (full only) |
| License Auditor | `security-license-auditor` | License compatibility, SBOM | Round 1 (compliance only) |
| Skeptic | `security-skeptic` | Attacks findings for FPs | Round 2 |
| Evaluator | `security-evaluator` | 5-dim quality gate | Round 3 |
| Retrospector | `security-retrospector` | Cross-session learning | Close |

## Tier classification

- **Quick scan**: 3 specialists (owasp, secrets, deps). <5 minutes.
- **Standard audit**: 5 specialists (+crypto, config). <15 minutes.
- **Full audit**: all 8 domain specialists. <30 minutes.
- **Compliance audit**: Full + license emphasis.

Default bias: when in doubt, pick the higher tier.

## Round structure

| Round | Name | Output |
|---|---|---|
| Round 0 | Intake + auto-detect | AUDIT_CHARTER.md |
| Round 1 | Domain specialists (parallel) | EVIDENCE/<specialist>.md |
| Round 2 | Skeptic gate | EVIDENCE/skeptic.md |
| Round 3 | Evaluator gate | EVIDENCE/evaluator.md + SECURITY_REPORT.md |
| Close | Retrospection + scribe | MEMORY.md updated |

## Verdict system

```
BLOCKER: any CRITICAL, or >=3 HIGH
ADVISORY: any HIGH or MEDIUM, and not BLOCKER
PASS: only LOW or no findings
```

| Verdict | Engineering action |
|---|---|
| BLOCKER | Must remediate before merge. |
| ADVISORY | Should remediate. Merge allowed with documented risk acceptance. |
| PASS | Clean to merge. |

## Finding schema (mandatory for all domain specialists)

Each finding MUST contain: severity (CRITICAL/HIGH/MEDIUM/LOW), category, location (file:line), exploitability, blast radius, confidence, description, evidence (code snippet), remediation (vulnerable vs fixed code), verification notes.

## Prior art

- OWASP Top 10 (2025) + OWASP Top 10 for Agentic Applications (2026)
- IRIS (arxiv 2405.17238) -- neuro-symbolic hybrid (SAST + LLM)
- ASTRIDE (arxiv 2512.04785) -- agentic AI threat modeling
- MITRE ATLAS v5.1 -- AI threat framework
- Engineering Team PROTOCOL v1 -- cross-team handoff, staging protocol
- MAST (Cemri et al., arxiv 2503.13657) -- failure mode taxonomy
