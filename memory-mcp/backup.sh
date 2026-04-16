#!/usr/bin/env bash
# WAL checkpoint + timestamped backup of the memory database.
# Uses Python's sqlite3 stdlib (no sqlite3 CLI required).
# Usage: bash backup.sh [backup_dir]
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB="${DIR}/memory.db"
BACKUP_DIR="${1:-${HOME}/.claude/backups/memory-mcp}"

if [ ! -f "${DB}" ]; then
    echo "ERROR: Database not found at ${DB}" >&2
    exit 1
fi

mkdir -p "${BACKUP_DIR}"
TIMESTAMP=$(date +"%Y-%m-%dT%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/memory_${TIMESTAMP}.db"

python3 - "${DB}" "${BACKUP_FILE}" <<'PYEOF'
import sqlite3
import sys
from pathlib import Path

src = sys.argv[1]
dst = sys.argv[2]

src_db = sqlite3.connect(src)
# WAL checkpoint first
src_db.execute("PRAGMA wal_checkpoint(TRUNCATE)")

# Online backup
dst_db = sqlite3.connect(dst)
src_db.backup(dst_db)
dst_db.close()
src_db.close()

size = Path(dst).stat().st_size
print(f"Backup written: {dst}")
print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")
PYEOF

# Prune backups older than 30 days
find "${BACKUP_DIR}" -name "memory_*.db" -mtime +30 -delete 2>/dev/null || true
echo "Old backups pruned (>30 days)."
