#!/usr/bin/env python3
"""meta_evaluator.py — aggregate metrics across research team sessions."""

import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SPECIALISTS = [
    "planner", "cartographer", "archaeologist", "librarian", "tracer",
    "empiricist", "linguist", "historian", "web-miner", "github-miner",
    "synthesist", "skeptic", "adversary", "moderator", "evaluator",
    "retrospector", "scribe"
]

GATES = ["planner", "synthesist", "moderator", "skeptic", "adversary", "evaluator", "retrospector"]


def find_sessions(project_dir):
    """Find all research session directories."""
    teams_dir = Path(project_dir) / ".claude" / "teams" / "research"
    if not teams_dir.exists():
        return []
    sessions = []
    for d in sorted(teams_dir.iterdir()):
        if d.is_dir() and (d / "EVIDENCE").is_dir() and not d.name.startswith("SMOKE"):
            sessions.append(d)
    return sessions


def analyze_session(session_dir):
    """Analyze a single session."""
    result = {
        "slug": session_dir.name,
        "specialists_present": [],
        "specialists_missing": [],
        "evidence_sizes": {},
        "confidence": "unknown",
        "evaluator_pass": None,
        "adversary_rejections": 0,
        "adversary_sources": 0,
        "round_count": 0,
    }

    evidence_dir = session_dir / "EVIDENCE"
    for spec in SPECIALISTS:
        f = evidence_dir / f"{spec}.md"
        if f.exists():
            result["specialists_present"].append(spec)
            result["evidence_sizes"][spec] = f.stat().st_size
        else:
            result["specialists_missing"].append(spec)

    # Parse SYNTHESIS for confidence
    syn = session_dir / "SYNTHESIS.md"
    if syn.exists():
        text = syn.read_text(errors="replace")
        if re.search(r"confidence.*high|HIGH", text, re.I):
            result["confidence"] = "HIGH"
        elif re.search(r"confidence.*medium|MEDIUM", text, re.I):
            result["confidence"] = "MEDIUM"
        elif re.search(r"confidence.*low|LOW", text, re.I):
            result["confidence"] = "LOW"

        # Count specialist citations in synthesis
        result["synthesis_citations"] = {}
        for spec in SPECIALISTS:
            count = len(re.findall(rf"\b{spec}\b", text, re.I))
            if count > 0:
                result["synthesis_citations"][spec] = count

    # Parse evaluator for pass/fail
    evalf = evidence_dir / "evaluator.md"
    if evalf.exists():
        etext = evalf.read_text(errors="replace")
        if re.search(r"PASS", etext):
            result["evaluator_pass"] = True
        elif re.search(r"FAIL", etext):
            result["evaluator_pass"] = False

    # Parse adversary for rejections
    advf = evidence_dir / "adversary.md"
    if advf.exists():
        atext = advf.read_text(errors="replace")
        result["adversary_rejections"] = len(re.findall(r"REJECT", atext))
        result["adversary_sources"] = len(re.findall(r"http[s]?://", atext))

    # Parse LOG for round count
    logf = session_dir / "LOG.md"
    if logf.exists():
        ltext = logf.read_text(errors="replace")
        result["round_count"] = len(re.findall(r"round|Round|ROUND", ltext))

    return result


def analyze_memory(memory_path):
    """Analyze MEMORY.md lessons."""
    if not memory_path.exists():
        return []
    text = memory_path.read_text(errors="replace")
    lessons = []
    for match in re.finditer(r"^### (.+)", text, re.MULTILINE):
        title = match.group(1).strip()
        # Find observed-in date
        section = text[match.start():match.start() + 500]
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", section)
        date = date_match.group(0) if date_match else "unknown"
        reinforced = len(re.findall(r"Reinforced by", section))
        lessons.append({"title": title, "date": date, "reinforced": reinforced})
    return lessons


def generate_report(sessions, analyses, lessons):
    """Generate the meta-evaluation report."""
    lines = []
    lines.append("# Meta-evaluation Report")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}")
    lines.append(f"Sessions analyzed: {len(analyses)}")
    if analyses:
        lines.append(f"Date range: {analyses[0]['slug']} .. {analyses[-1]['slug']}")
    lines.append("")

    # Gate load-bearing analysis
    lines.append("## Gate Load-bearing Analysis")
    lines.append("| Gate | Present | Absent | Cited in synthesis | Verdict |")
    lines.append("|------|---------|--------|-------------------|---------|")
    for gate in GATES:
        present = sum(1 for a in analyses if gate in a["specialists_present"])
        absent = sum(1 for a in analyses if gate in a["specialists_missing"])
        cited = sum(1 for a in analyses if a.get("synthesis_citations", {}).get(gate, 0) > 0)
        ratio = cited / max(present, 1)
        verdict = "LOAD-BEARING" if ratio > 0.3 else ("THEATER" if ratio < 0.1 and present > 2 else "NORMAL")
        lines.append(f"| {gate} | {present} | {absent} | {cited} ({ratio:.0%}) | {verdict} |")
    lines.append("")

    # Specialist citation ranking
    lines.append("## Specialist Citation Ranking")
    lines.append("| Specialist | Present | Cited | Ratio | Median KB | Verdict |")
    lines.append("|-----------|---------|-------|-------|-----------|---------|")
    for spec in SPECIALISTS:
        present = sum(1 for a in analyses if spec in a["specialists_present"])
        cited = sum(1 for a in analyses if a.get("synthesis_citations", {}).get(spec, 0) > 0)
        sizes = [a["evidence_sizes"].get(spec, 0) for a in analyses if spec in a["specialists_present"]]
        median_kb = sorted(sizes)[len(sizes)//2] / 1024 if sizes else 0
        ratio = cited / max(present, 1)
        verdict = "HIGH-VALUE" if ratio > 0.7 and median_kb > 3 else ("LOW-VALUE" if ratio < 0.3 and present > 2 else "NORMAL")
        lines.append(f"| {spec} | {present} | {cited} | {ratio:.0%} | {median_kb:.1f} | {verdict} |")
    lines.append("")

    # Adversary effectiveness
    lines.append("## Adversary Effectiveness")
    lines.append("| Session | Sources | Rejections | Rate | Verdict |")
    lines.append("|---------|---------|------------|------|---------|")
    for a in analyses:
        if "adversary" in a["specialists_present"]:
            rate = a["adversary_rejections"] / max(a["adversary_sources"], 1)
            verdict = "ACTIVE" if rate > 0.05 or a["adversary_rejections"] > 0 else "RUBBER-STAMP"
            lines.append(f"| {a['slug'][:40]} | {a['adversary_sources']} | {a['adversary_rejections']} | {rate:.0%} | {verdict} |")
    lines.append("")

    # Quality trend
    lines.append("## Session Quality Summary")
    lines.append("| Session | Specialists | Evidence KB | Confidence | Evaluator |")
    lines.append("|---------|------------|-------------|------------|-----------|")
    for a in analyses:
        total_kb = sum(a["evidence_sizes"].values()) / 1024
        ev_pass = "PASS" if a["evaluator_pass"] else ("FAIL" if a["evaluator_pass"] is False else "N/A")
        lines.append(f"| {a['slug'][:40]} | {len(a['specialists_present'])}/{len(SPECIALISTS)} | {total_kb:.0f} | {a['confidence']} | {ev_pass} |")
    lines.append("")

    # MEMORY lesson status
    if lessons:
        lines.append("## MEMORY.md Lessons")
        lines.append(f"Total lessons: {len(lessons)}")
        lines.append(f"Reinforced (>0): {sum(1 for l in lessons if l['reinforced'] > 0)}")
        lines.append(f"Never reinforced: {sum(1 for l in lessons if l['reinforced'] == 0)}")
        lines.append("")

    return "\n".join(lines)


def main():
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    sessions = find_sessions(project_dir)

    if not sessions:
        print(f"No research sessions found in {project_dir}/.claude/teams/research/")
        sys.exit(0)

    analyses = [analyze_session(s) for s in sessions]
    memory_path = Path.home() / ".claude" / "agent-memory" / "research-lead" / "MEMORY.md"
    lessons = analyze_memory(memory_path)

    report = generate_report(sessions, analyses, lessons)
    print(report)

    # Write to file
    out_path = Path(project_dir) / ".claude" / "teams" / "research" / "META_EVAL.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    print(f"\nReport written to: {out_path}")


if __name__ == "__main__":
    main()
