#!/usr/bin/env python3
"""
audit_evidence.py — Evidence-file-as-contract gate for the Research Team.

Checks a session workspace against its EXPECTED_EVIDENCE.md contract and reports
PASS/FAIL with specific violations per specialist. Stdlib only (Python 3.11+).

Usage:
    python3 audit_evidence.py <slug>                          # full audit, synthesis gate
    python3 audit_evidence.py <slug> --gate=mid-flight        # soft gate (missing OK)
    python3 audit_evidence.py <slug> --strict                 # add smear detection
    python3 audit_evidence.py <slug> --team=research          # select team
    python3 audit_evidence.py <slug> --format=json            # machine-readable
    python3 audit_evidence.py <slug> --verbose                # include file metadata

Exit codes:
    0  PASS — every expected file exists and satisfies the schema
    1  FAIL — one or more violations; details on stdout
    2  ERROR — script itself failed (missing dir, parse error)

Integration:
    - Called by research-lead via Bash before writing SYNTHESIS.md (synthesis gate)
    - Called by research-lead between rounds (mid-flight gate)
    - Called by retrospector at session close for the compliance grade
    - Called by the smoke test to validate a deliberately-shortcut session
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# --- SCHEMA CONSTANTS (v2.1) ---
# Calibrated empirically 2026-04-12 against 3 real sessions (49 files total)

# Minimum bytes for a lens role. Tuned low enough that honest-but-brief passes
# are allowed, high enough that stubs fail.
MIN_LENS_BYTES = 2_000
MIN_LEDGER_BYTES = 1_500

# Role categories — calibrated empirically 2026-04-12 against 49 real files.
# Ledger roles: curate/index, not investigate. Relaxed thresholds.
LEDGER_ROLES = frozenset({"scribe", "planner"})

# Local lens roles: grep/read filesystem, tests, git history. Their "citations"
# are paths + inline code + observed facts, not URLs. Lower citation threshold.
LOCAL_LENS_ROLES = frozenset({
    "cartographer", "archaeologist", "tracer", "linguist",
})

# External-source lens roles: URL/arxiv/issue/code citations expected.
EXTERNAL_LENS_ROLES = frozenset({
    "librarian", "historian", "web-miner", "github-miner", "empiricist",
})

# Integration/adversarial lens roles: cite sibling evidence files, not external.
INTEGRATION_ROLES = frozenset({
    "synthesist", "skeptic", "adversary", "moderator", "evaluator", "retrospector",
})

# Every evidence file (lens or ledger) must have at least this many distinct H2
# sections. Empirically real files have 6-15 H2s; stubs have ≤ 2.
MIN_H2_SECTIONS_LENS = 4
MIN_H2_SECTIONS_LEDGER = 3

# Minimum distinct citation tokens, per role category:
#   external lens: 3+ URL/arxiv/issue/code citations (hard-external)
#   integration:   2+ cross-file refs (EVIDENCE/*.md, #N, [Cx], etc)
#   local lens:    1+ path/command/grep observation (allows filesystem-heavy passes)
#   ledger:        0
MIN_CITATIONS_LOCAL_LENS = 1
MIN_CITATIONS_INTEGRATION = 2
MIN_CITATIONS_EXTERNAL_LENS = 3
MIN_CITATIONS_LEDGER = 0

# Terminal "confidence" or "handoff" section: every lens file should end with
# either a `## Confidence` or `## Handoff` or `## Verdict` header. This is a
# calibration signal that the author actually thought about the end-state of
# the pass, not just dumped findings. Ledger roles also tend to have this.
TERMINAL_SECTION_PATTERNS = [
    r"^##\s+.*confidence",
    r"^##\s+.*handoff",
    r"^##\s+.*verdict",
    r"^##\s+.*handoffs?\s+and\s+open",
    r"^##\s+.*summary",
]

# Method-like opener section. Should be among the first 5 H2 sections.
# (Used as soft signal, not hard requirement — enforced only in --strict.)
OPENER_SECTION_PATTERNS = [
    r"^##\s+.*method",
    r"^##\s+.*approach",
    r"^##\s+.*scope",
    r"^##\s+.*why\s+this\s+pass",
    r"^##\s+.*recommendation",
    r"^##\s+.*plan",
    r"^##\s+.*question\s+class",
    r"^##\s+.*inventory",
    r"^##\s+.*classification",
]

# v2.1 YAML frontmatter schema. Absence is LEGACY (grandfathered v2 files).
# Presence of all fields bumps "schema_version" to v2.1 in the report.
FRONTMATTER_FIELDS_V21 = [
    "specialist", "slug", "started", "completed",
    "tool_calls_count", "citations_count", "confidence",
]

# Smear detection: Jaccard similarity above which two evidence files are
# considered lexically suspiciously-close (potential lead-generalist-smear).
# Tuned empirically against real sibling sessions: honest-but-related pairs
# (librarian ~ historian in memory-layer session) measured 0.25-0.45. A smear
# would be > 0.6. Threshold 0.60 is strict but not reckless.
JACCARD_THRESHOLD = 0.60
# Stopwords for signature: generic English + multi-agent common terms so the
# baseline lexicon doesn't dominate the signal.
STOPWORDS = frozenset("""
a an the and or but if then is are was were be been being of in on at by for with
to from as that this these those it its we they he she i you them our your their
which who whom what when where why how not no do does did can could should would
may might must one two three first second also such said have has had will
research specialist evidence session slug sub question team file files writes
wrote method findings confidence citations handoff handoffs open source
claude anthropic protocol agent agents subagent subagents lead lead's
""".split())


@dataclass
class FileViolation:
    specialist: str
    path: Path
    kind: str      # missing | too_small | too_few_sections | no_terminal | too_few_citations | smear_signature
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {
            "specialist": self.specialist,
            "path": str(self.path),
            "kind": self.kind,
            "detail": self.detail,
        }


@dataclass
class FileMeta:
    specialist: str
    path: Path
    exists: bool
    size: int = 0
    h2_count: int = 0
    citations: int = 0
    has_frontmatter: bool = False
    schema_version: str = "v2-legacy"
    frontmatter: dict[str, str] = field(default_factory=dict)
    has_terminal_section: bool = False
    has_opener_section: bool = False
    tokens: set[str] = field(default_factory=set)

    def as_dict(self) -> dict[str, Any]:
        return {
            "specialist": self.specialist,
            "exists": self.exists,
            "size": self.size,
            "h2_count": self.h2_count,
            "citations": self.citations,
            "has_frontmatter": self.has_frontmatter,
            "schema_version": self.schema_version,
            "has_terminal_section": self.has_terminal_section,
            "has_opener_section": self.has_opener_section,
        }


@dataclass
class AuditResult:
    slug: str
    workspace: Path
    team: str
    gate: str
    expected: list[str]
    present: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    legacy_files: list[str] = field(default_factory=list)
    v21_files: list[str] = field(default_factory=list)
    violations: list[FileViolation] = field(default_factory=list)
    metadata: dict[str, FileMeta] = field(default_factory=dict)
    total_bytes: int = 0
    smear_detected: bool = False
    smear_pairs: list[tuple[str, str, float]] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        if self.gate == "synthesis":
            return not self.missing and not self.violations
        # mid-flight: missing is OK, but existing files must still pass schema
        return not self.violations

    def as_dict(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "workspace": str(self.workspace),
            "team": self.team,
            "gate": self.gate,
            "passed": self.passed,
            "expected": self.expected,
            "present": self.present,
            "missing": self.missing,
            "legacy_files": self.legacy_files,
            "v21_files": self.v21_files,
            "total_bytes": self.total_bytes,
            "file_sizes": {s: m.size for s, m in self.metadata.items() if m.exists},
            "violations": [v.as_dict() for v in self.violations],
            "smear_detected": self.smear_detected,
            "smear_pairs": [
                {"a": a, "b": b, "jaccard": round(sim, 4)}
                for a, b, sim in self.smear_pairs
            ],
        }


# --- CONTRACT RESOLUTION ---

def load_expected(workspace: Path, team: str = "research") -> list[str]:
    """Read EXPECTED_EVIDENCE.md if present (one specialist name per line, '-' or
    '*' bullets stripped, '#' comments ignored). Otherwise fall back to team
    roster."""
    expected_file = workspace / "EXPECTED_EVIDENCE.md"
    if expected_file.exists():
        out: list[str] = []
        for line in expected_file.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r"^[-*]\s*", "", line)
            line = re.sub(r"\.md$", "", line)
            if line and re.match(r"^[a-z][a-z0-9_-]+$", line):
                out.append(line)
        if out:
            return out

    return default_expected(team)


def default_expected(team: str = "research") -> list[str]:
    """Default expected-specialist list per team. Extend as new teams are added."""
    if team == "research":
        return [
            "planner",
            "cartographer", "archaeologist", "tracer", "linguist",
            "librarian", "historian", "web-miner", "github-miner",
            "empiricist",
            "synthesist",
            "skeptic", "adversary", "moderator",
            "evaluator",
            "retrospector", "scribe",
        ]
    if team == "engineering":
        # Placeholder — the engineering-team-self-evolve-v1 session will define
        # the canonical engineering roster. This is a stub.
        return [
            "planner", "architect", "executor", "verifier", "reviewer",
            "skeptic", "adversary", "moderator", "evaluator",
            "retrospector", "scribe",
        ]
    return []


# --- FILE PARSING ---

def split_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Parse YAML-ish frontmatter at the top of a markdown file. Simple
    key: value pairs only; no nested structures. Returns (dict | None, body)."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if len(lines) < 3:
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fm: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        k, _, v = raw.partition(":")
        fm[k.strip()] = v.strip()
    body = "\n".join(lines[end + 1:])
    return fm, body


def count_h2_sections(body: str) -> int:
    """Count distinct '## ' level-2 headers."""
    return len(re.findall(r"^##\s+\S", body, flags=re.MULTILINE))


def count_citations(body: str) -> int:
    """Count distinct citation tokens. Supports: URLs, arxiv IDs, GitHub issue
    numbers, bracketed refs, path:line, retrieved dates, cross-file refs, and
    inline commands for filesystem passes. Case-insensitive."""
    seen: set[str] = set()
    patterns = [
        r"https?://\S+",                    # URLs
        r"arxiv[\s:/]*\d{4}\.\d{4,5}",      # arxiv IDs
        r"\[[A-Za-z][A-Za-z0-9]{0,5}:?\d{1,4}\]",  # [G1] [fs:12] [H14]
        r"#\d{3,6}\b",                      # github issue/PR numbers
        r"\brepo:[\w./-]+\b",               # gh search repo:foo/bar
        r"`[\w./-]+?:\d+`",                 # `src/foo.py:123` citations
        r"retrieved\s+\d{4}-\d{2}-\d{2}",   # retrieved-date markers
        r"EVIDENCE/[\w-]+\.md",             # cross-file refs to sibling evidence
        r"`ls\s+[^`]+`",                    # `ls /some/path` filesystem observations
        r"`grep\s+[^`]+`",                  # `grep pattern path` observations
        r"`find\s+[^`]+`",                  # `find path …` observations
        r"~?/[\w.-]+(?:/[\w.-]+)+",         # absolute or ~-relative paths (≥ 2 segments)
        r"PROTOCOL\.md",                    # protocol reference
        r"MEMORY\.md",                      # memory reference
        r"`[A-Za-z_][A-Za-z0-9_.]+\(\)`",   # function refs `foo()`, `_R()`
    ]
    for pat in patterns:
        for m in re.findall(pat, body, flags=re.IGNORECASE):
            seen.add(m.lower())
    return len(seen)


def has_terminal_section(body: str) -> bool:
    """Check whether any terminal (confidence/handoff/verdict) section exists."""
    return any(
        re.search(pat, body, flags=re.IGNORECASE | re.MULTILINE)
        for pat in TERMINAL_SECTION_PATTERNS
    )


def has_opener_section(body: str) -> bool:
    """Check whether a method-like opener exists in the first 5 H2 headers."""
    headers = re.findall(r"^##\s+.*", body, flags=re.MULTILINE)[:5]
    opener_block = "\n".join(headers)
    return any(
        re.search(pat, opener_block, flags=re.IGNORECASE | re.MULTILINE)
        for pat in OPENER_SECTION_PATTERNS
    )


def tokenize_for_signature(body: str) -> set[str]:
    """Lowercase unigrams for Jaccard signature."""
    words = re.findall(r"\b[a-z][a-z'-]{2,}\b", body.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def detect_schema_version(fm: dict[str, str] | None) -> str:
    if fm is None:
        return "v2-legacy"
    missing = [f for f in FRONTMATTER_FIELDS_V21 if f not in fm]
    if not missing:
        return "v2.1"
    return "v2-partial"


# --- AUDIT ---

def audit_file(specialist: str, path: Path) -> FileMeta:
    """Audit a single evidence file and return populated metadata."""
    meta = FileMeta(specialist=specialist, path=path, exists=path.exists())
    if not meta.exists:
        return meta

    raw = path.read_text(encoding="utf-8", errors="replace")
    meta.size = len(raw.encode("utf-8"))

    fm, body = split_frontmatter(raw)
    meta.has_frontmatter = fm is not None
    meta.frontmatter = fm or {}
    meta.schema_version = detect_schema_version(fm)

    meta.h2_count = count_h2_sections(body)
    meta.citations = count_citations(body)
    meta.has_terminal_section = has_terminal_section(body)
    meta.has_opener_section = has_opener_section(body)
    meta.tokens = tokenize_for_signature(body)
    return meta


def role_thresholds(specialist: str) -> tuple[int, int, int, str]:
    """Return (min_bytes, min_h2, min_citations, category_label) for a specialist."""
    if specialist in LEDGER_ROLES:
        return MIN_LEDGER_BYTES, MIN_H2_SECTIONS_LEDGER, MIN_CITATIONS_LEDGER, "ledger"
    if specialist in LOCAL_LENS_ROLES:
        return MIN_LENS_BYTES, MIN_H2_SECTIONS_LENS, MIN_CITATIONS_LOCAL_LENS, "local-lens"
    if specialist in EXTERNAL_LENS_ROLES:
        return MIN_LENS_BYTES, MIN_H2_SECTIONS_LENS, MIN_CITATIONS_EXTERNAL_LENS, "external-lens"
    if specialist in INTEGRATION_ROLES:
        return MIN_LENS_BYTES, MIN_H2_SECTIONS_LENS, MIN_CITATIONS_INTEGRATION, "integration"
    # Unknown specialist: treat as generic lens with conservative defaults
    return MIN_LENS_BYTES, MIN_H2_SECTIONS_LENS, MIN_CITATIONS_EXTERNAL_LENS, "unknown-lens"


def violations_for(meta: FileMeta) -> list[FileViolation]:
    """Derive violations from a file's metadata against the schema."""
    vios: list[FileViolation] = []
    if not meta.exists:
        vios.append(FileViolation(
            meta.specialist, meta.path, "missing",
            f"File does not exist: {meta.path}",
        ))
        return vios

    min_bytes, min_h2, min_cites, category = role_thresholds(meta.specialist)

    if meta.size < min_bytes:
        vios.append(FileViolation(
            meta.specialist, meta.path, "too_small",
            f"{meta.size} bytes < {min_bytes} minimum for {category} role",
        ))
    if meta.h2_count < min_h2:
        vios.append(FileViolation(
            meta.specialist, meta.path, "too_few_sections",
            f"{meta.h2_count} H2 sections < {min_h2} minimum (structural depth signal)",
        ))
    if meta.citations < min_cites:
        vios.append(FileViolation(
            meta.specialist, meta.path, "too_few_citations",
            f"{meta.citations} distinct citation tokens < {min_cites} minimum for {category} role",
        ))
    if not meta.has_terminal_section:
        vios.append(FileViolation(
            meta.specialist, meta.path, "no_terminal",
            "no ## Confidence / ## Handoff / ## Verdict terminal section (end-state signal)",
        ))
    return vios


def resolve_workspace(slug: str, team: str = "research") -> Path:
    """Resolve session workspace path.

    Resolution order (v2.1 scope model):
    1. <cwd>/.claude/teams/<team>/<slug>/ — per-project (preferred)
    2. ~/.claude/teams/<team>/<slug>/     — legacy global (fallback)

    Raises FileNotFoundError if neither exists.
    """
    cwd_path = Path.cwd() / ".claude" / "teams" / team / slug
    if cwd_path.exists():
        return cwd_path
    global_path = Path.home() / ".claude" / "teams" / team / slug
    if global_path.exists():
        return global_path
    raise FileNotFoundError(
        f"Workspace not found: tried {cwd_path} (per-project) "
        f"and {global_path} (legacy global)"
    )


def audit_workspace(slug: str, team: str = "research", gate: str = "synthesis",
                    strict: bool = False) -> AuditResult:
    workspace = resolve_workspace(slug, team)
    if not workspace.exists():
        raise FileNotFoundError(f"Workspace not found: {workspace}")

    expected = load_expected(workspace, team)
    result = AuditResult(
        slug=slug, workspace=workspace, team=team, gate=gate, expected=expected,
    )
    evidence_dir = workspace / "EVIDENCE"
    if not evidence_dir.exists():
        result.missing = expected[:]
        if gate == "synthesis":
            for spec in expected:
                result.violations.append(FileViolation(
                    spec, evidence_dir / f"{spec}.md", "missing",
                    "EVIDENCE/ directory does not exist",
                ))
        return result

    for specialist in expected:
        path = evidence_dir / f"{specialist}.md"
        # Support -addendum.md variant from memory-layer session
        if not path.exists():
            addendum = evidence_dir / f"{specialist}-addendum.md"
            if addendum.exists():
                path = addendum
        meta = audit_file(specialist, path)
        result.metadata[specialist] = meta
        if meta.exists:
            result.present.append(specialist)
            result.total_bytes += meta.size
            if meta.schema_version == "v2.1":
                result.v21_files.append(specialist)
            else:
                result.legacy_files.append(specialist)
            result.violations.extend(violations_for(meta))
        else:
            result.missing.append(specialist)
            if gate == "synthesis":
                result.violations.extend(violations_for(meta))

    if strict:
        specs_with_tokens = [
            (s, m) for s, m in result.metadata.items() if m.exists and m.tokens
        ]
        for i in range(len(specs_with_tokens)):
            for j in range(i + 1, len(specs_with_tokens)):
                a_name, a_meta = specs_with_tokens[i]
                b_name, b_meta = specs_with_tokens[j]
                sim = jaccard(a_meta.tokens, b_meta.tokens)
                if sim >= JACCARD_THRESHOLD:
                    result.smear_pairs.append((a_name, b_name, sim))
                    result.violations.append(FileViolation(
                        a_name, a_meta.path, "smear_signature",
                        f"Jaccard similarity {sim:.3f} with {b_name}.md ≥ threshold {JACCARD_THRESHOLD} (possible lead-generalist-smear)",
                    ))
        result.smear_pairs.sort(key=lambda p: -p[2])
        result.smear_detected = bool(result.smear_pairs)

    return result


# --- OUTPUT ---

def format_text(result: AuditResult, verbose: bool = False) -> str:
    lines: list[str] = []
    lines.append(f"=== Evidence Audit: {result.slug} (team={result.team}, gate={result.gate}) ===")
    lines.append(f"Workspace:     {result.workspace}")
    lines.append(f"Expected:      {len(result.expected)}")
    lines.append(f"Present:       {len(result.present)} ({', '.join(result.present) or '(none)'})")
    lines.append(f"Missing:       {len(result.missing)} ({', '.join(result.missing) or '(none)'})")
    lines.append(f"Schema v2.1:   {len(result.v21_files)} ({', '.join(result.v21_files) or '(none)'})")
    lines.append(f"Schema legacy: {len(result.legacy_files)} (no frontmatter, grandfathered)")
    lines.append(f"Total bytes:   {result.total_bytes:,}")
    lines.append(f"Violations:    {len(result.violations)}")

    if verbose:
        lines.append("")
        lines.append("--- Per-file metadata ---")
        for spec in result.expected:
            m = result.metadata.get(spec)
            if not m or not m.exists:
                lines.append(f"  {spec:20s} MISSING")
                continue
            lines.append(
                f"  {spec:20s} {m.size:7d}B  {m.h2_count:3d}H2  {m.citations:3d}cites  "
                f"{'fm=' + m.schema_version:<18s}  "
                f"{'term' if m.has_terminal_section else '----'}  "
                f"{'open' if m.has_opener_section else '----'}"
            )

    if result.violations:
        lines.append("")
        lines.append("--- Violations ---")
        for v in result.violations:
            lines.append(f"  [{v.kind}] {v.specialist}: {v.detail}")

    if result.smear_detected:
        lines.append("")
        lines.append("--- Smear detection (strict mode) ---")
        for a, b, sim in result.smear_pairs:
            lines.append(f"  similarity {sim:.3f}: {a}.md ~ {b}.md")

    lines.append("")
    lines.append(f"RESULT: {'PASS' if result.passed else 'FAIL'}")
    return "\n".join(lines)


def format_json(result: AuditResult) -> str:
    return json.dumps(result.as_dict(), indent=2)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Audit a research session's EVIDENCE/ directory against the evidence-file-as-contract schema.",
    )
    ap.add_argument("slug", help="Session slug. Resolved: <cwd>/.claude/teams/<team>/<slug>/ first, then ~/.claude/teams/<team>/<slug>/ as legacy fallback.")
    ap.add_argument("--team", default="research", help="Team name (default: research)")
    ap.add_argument("--gate", choices=["synthesis", "mid-flight"], default="synthesis",
                    help="synthesis=strict on missing, mid-flight=warn on missing")
    ap.add_argument("--strict", action="store_true",
                    help="Enable vocabulary-signature smear detection (Jaccard > 0.60)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--verbose", "-v", action="store_true", help="Include per-file metadata")
    args = ap.parse_args(argv)

    try:
        result = audit_workspace(args.slug, team=args.team, gate=args.gate, strict=args.strict)
    except FileNotFoundError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"ERROR: {type(e).__name__}: {e}\n")
        return 2

    out = format_json(result) if args.format == "json" else format_text(result, verbose=args.verbose)
    print(out)
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
