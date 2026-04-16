#!/usr/bin/env bash
# Bootstrap the memory MCP database from existing MEMORY.md files.
# Uses Python's sqlite3 stdlib (no sqlite3 CLI required).
# Safe to re-run — skips already-imported content.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_MEMORY_ROOT="${HOME}/.claude/agent-memory"

python3 - "${DIR}" "${AGENT_MEMORY_ROOT}" <<'PYEOF'
import sqlite3
import re
import sys
import os
from pathlib import Path

script_dir = Path(sys.argv[1])
agent_memory_root = Path(sys.argv[2])
db_path = script_dir / "memory.db"
schema_path = script_dir / "schema.sql"

print("=== Memory MCP Bootstrap ===")
print(f"DB:     {db_path}")
print(f"Schema: {schema_path}")
print()

# Create DB and apply schema
db = sqlite3.connect(str(db_path))
db.row_factory = sqlite3.Row
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA synchronous=NORMAL")
db.execute("PRAGMA foreign_keys=ON")

# Check FTS5 support
try:
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _fts5_test USING fts5(x)")
    db.execute("DROP TABLE IF EXISTS _fts5_test")
    print("FTS5: available")
except Exception as e:
    print(f"WARNING: FTS5 not available: {e}")

db.executescript(schema_path.read_text())
print("Schema applied.")
print()

total_imported = 0

if not agent_memory_root.exists():
    print(f"No agent-memory directory found at {agent_memory_root}")
else:
    for agent_dir in sorted(agent_memory_root.iterdir()):
        if not agent_dir.is_dir():
            continue
        memory_file = agent_dir / "MEMORY.md"
        if not memory_file.exists():
            continue

        agent = agent_dir.name
        print(f"Importing {agent}...")

        content = memory_file.read_text(errors="replace")

        # Split on ### headers
        sections = re.split(r"(?m)^### ", content)
        count = 0
        for section in sections[1:]:   # sections[0] is preamble
            lines = section.strip().splitlines()
            if not lines:
                continue

            title = lines[0].strip()
            body = "### " + section.strip()

            # Extract tags from "Failure mode addressed:" or "Tags:" lines
            tags = ""
            fm_match = re.search(
                r"(?:Failure mode addressed|Tags).*?:\s*(.*)",
                body,
                re.IGNORECASE
            )
            if fm_match:
                tags = fm_match.group(1).strip()

            # Heuristic lesson_type from title
            lt = "lesson"
            lower = title.lower()
            if any(w in lower for w in ("warning", "never", "avoid", "danger")):
                lt = "warning"
            elif any(w in lower for w in ("pattern", "always use", "always ")):
                lt = "pattern"
            elif any(w in lower for w in ("principle", "core ", "fundamental")):
                lt = "core-principle"

            # Skip duplicates
            existing = db.execute(
                "SELECT id FROM memories WHERE source_agent=? AND content=?",
                (agent, body)
            ).fetchone()
            if existing:
                continue

            db.execute(
                "INSERT INTO memories (content, source_agent, lesson_type, tags) VALUES (?, ?, ?, ?)",
                (body, agent, lt, tags)
            )
            count += 1

        db.commit()
        print(f"  Imported {count} new lessons from {agent}")
        total_imported += count

db.commit()

# Final stats
total_in_db = db.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
db_size = db_path.stat().st_size

print()
print(f"Import complete. New entries: {total_imported}")
print(f"Total in DB:   {total_in_db}")
print(f"DB size:       {db_size:,} bytes ({db_size/1024:.1f} KB)")
print()

# Per-agent breakdown
rows = db.execute(
    "SELECT source_agent, COUNT(*) as cnt FROM memories GROUP BY source_agent ORDER BY cnt DESC"
).fetchall()
if rows:
    print("Breakdown by agent:")
    for r in rows:
        print(f"  {r[0]:30s} {r[1]:4d}")

db.close()
print()
print("Bootstrap complete.")
PYEOF
