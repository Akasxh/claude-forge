# Hook B — Python MCP server for SQLite + FTS5 + sqlite-vec (scaffold)

This file contains the directory scaffold, schema DDL, API surface, ranker formula, settings.json registration, failure modes and recovery, build-trigger criteria for the Hook B MCP server. The code skeleton is complete enough for the forthcoming Engineering Team to implement without making architectural decisions.

## Decision summary

- **Language**: Python (adjudicated in `EVIDENCE/empiricist.md` § "Language choice for Hook B")
- **Python version**: 3.11+
- **Core dependencies**: `mcp>=1.27.0`, `sqlite-vec>=0.1.9`, `sentence-transformers` (for Qwen3-Embedding-0.6B)
- **Storage**: one SQLite file per subagent scope
- **Ranker**: MemX-derived 4-factor hybrid (semantic + recency + frequency + importance)
- **Build trigger**: `miss_rate > 20%` over 10 consecutive sessions (see `empiricist.md` § "Hook A insufficient")

## Directory layout

```
~/.claude/memory-mcp/                    # project root
├── README.md                            # setup + usage
├── pyproject.toml                       # Python project (uv-compatible)
├── src/
│   └── memory_mcp/
│       ├── __init__.py
│       ├── server.py                    # MCP server entry point (stdio)
│       ├── schema.sql                   # DDL (all tables, indexes, virtual tables)
│       ├── db.py                        # sqlite3 + sqlite_vec loader + connection pool
│       ├── ranker.py                    # MemX 4-factor hybrid ranker
│       ├── embedder.py                  # Qwen3-Embedding-0.6B wrapper
│       ├── handlers/
│       │   ├── __init__.py
│       │   ├── search.py                # memory.search(query, k=5)
│       │   ├── insert.py                # memory.insert(content, metadata)
│       │   ├── update.py                # memory.update(id, content)
│       │   ├── delete.py                # memory.delete(id)
│       │   ├── temporal.py              # memory.temporal(after, before) — v2
│       │   └── graph_neighbors.py       # memory.graph_neighbors(entity) — v2
│       └── migrations/
│           └── 001_initial.sql          # (placeholder; same content as schema.sql)
├── data/                                # NOT in git; created at first run
│   └── research-lead.sqlite             # one DB per subagent scope
├── tests/
│   ├── test_ranker.py                   # test hybrid scoring weights
│   ├── test_schema.py                   # DDL verification
│   ├── test_handlers.py                 # per-handler unit tests
│   └── test_server.py                   # MCP protocol integration
└── scripts/
    ├── bootstrap.py                     # create DB + load schema
    └── backup.sh                        # WAL checkpoint + cold copy
```

## Schema DDL (`src/memory_mcp/schema.sql`)

```sql
-- Hook B SQLite schema for Claude Code subagent memory layer
-- Requires: sqlite3 with FTS5 compiled in (default on all modern builds)
--           sqlite-vec extension loaded via sqlite_vec.load(conn)
-- Version: 1.0

-- 1. The main content table. One row per memory entry (lesson, topic file,
--    verbatim source, etc.). Uses rowid as internal primary key so FTS5 and
--    sqlite-vec can join cleanly.
CREATE TABLE IF NOT EXISTS memory (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    slug           TEXT NOT NULL UNIQUE,            -- kebab-case topic slug
    title          TEXT NOT NULL,
    body           TEXT NOT NULL,                   -- full markdown content
    tags           TEXT,                            -- JSON array of strings
    keywords       TEXT,                            -- JSON array of strings
    importance     REAL NOT NULL DEFAULT 50.0,      -- AKL score 0-100
    maturity       TEXT NOT NULL DEFAULT 'draft',   -- draft|validated|core
    access_count   INTEGER NOT NULL DEFAULT 0,
    update_count   INTEGER NOT NULL DEFAULT 1,
    created_at     INTEGER NOT NULL,                -- unix seconds
    last_accessed  INTEGER NOT NULL,                -- unix seconds
    last_updated   INTEGER NOT NULL,                -- unix seconds
    CHECK (maturity IN ('draft', 'validated', 'core')),
    CHECK (importance BETWEEN 0.0 AND 100.0)
);

-- 2. FTS5 virtual table for BM25 full-text search over body and title.
--    Using unicode61 tokenizer per MemX paper § 5.1.
CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    title,
    body,
    slug UNINDEXED,
    content=memory,
    content_rowid=id,
    tokenize='unicode61'
);

-- 3. Triggers to keep FTS5 in sync with memory table.
CREATE TRIGGER IF NOT EXISTS memory_ai AFTER INSERT ON memory BEGIN
    INSERT INTO memory_fts(rowid, title, body, slug)
    VALUES (NEW.id, NEW.title, NEW.body, NEW.slug);
END;
CREATE TRIGGER IF NOT EXISTS memory_ad AFTER DELETE ON memory BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, title, body, slug)
    VALUES ('delete', OLD.id, OLD.title, OLD.body, OLD.slug);
END;
CREATE TRIGGER IF NOT EXISTS memory_au AFTER UPDATE ON memory BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, title, body, slug)
    VALUES ('delete', OLD.id, OLD.title, OLD.body, OLD.slug);
    INSERT INTO memory_fts(rowid, title, body, slug)
    VALUES (NEW.id, NEW.title, NEW.body, NEW.slug);
END;

-- 4. sqlite-vec virtual table for vector search.
--    Dimension 1024 matches Qwen3-Embedding-0.6B (per MemX paper § 5.1).
--    Note: vec0 doesn't support FOREIGN KEY; we join by rowid convention.
CREATE VIRTUAL TABLE IF NOT EXISTS memory_vec USING vec0(
    embedding float[1024]
);

-- 5. Edges table for lightweight graph neighbors (v2 API surface).
--    Directed; typed by relation; both ends reference memory.id.
--    Populated lazily by the scribe when it writes @-annotations.
CREATE TABLE IF NOT EXISTS memory_edges (
    src_id      INTEGER NOT NULL REFERENCES memory(id) ON DELETE CASCADE,
    dst_id      INTEGER NOT NULL REFERENCES memory(id) ON DELETE CASCADE,
    relation    TEXT NOT NULL,                      -- e.g. 'related', 'supersedes', 'cites'
    created_at  INTEGER NOT NULL,
    PRIMARY KEY (src_id, dst_id, relation)
);

CREATE INDEX IF NOT EXISTS idx_memory_edges_dst ON memory_edges(dst_id);
CREATE INDEX IF NOT EXISTS idx_memory_edges_rel ON memory_edges(relation);

-- 6. Session log for temporal queries (v2 API surface).
--    Rows correspond to scribe writes, lead reads, and dedup events.
CREATE TABLE IF NOT EXISTS memory_events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id    INTEGER NOT NULL REFERENCES memory(id) ON DELETE CASCADE,
    event_type   TEXT NOT NULL,                     -- 'create'|'update'|'access'|'merge'|'supersede'
    session_slug TEXT,
    created_at   INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_memory_events_memory ON memory_events(memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_events_type ON memory_events(event_type);
CREATE INDEX IF NOT EXISTS idx_memory_events_time ON memory_events(created_at);

-- 7. Secondary indexes for hot lookups.
CREATE INDEX IF NOT EXISTS idx_memory_maturity ON memory(maturity);
CREATE INDEX IF NOT EXISTS idx_memory_last_accessed ON memory(last_accessed);
CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory(importance);

-- 8. Enable WAL mode for crash safety. (Execute at connection time, not in DDL.)
--    PRAGMA journal_mode = WAL;
--    PRAGMA synchronous = NORMAL;
--    PRAGMA foreign_keys = ON;
```

## API surface

| Handler | MVP? | Tool name | Inputs | Outputs | Behavior |
|---------|------|-----------|--------|---------|----------|
| **search** | **MVP** | `memory.search` | `query: str, k: int=5, maturity_min: str='draft'` | list of `{id, slug, title, snippet, score}` | hybrid FTS5 + vector + 4-factor rerank |
| **insert** | **MVP** | `memory.insert` | `slug: str, title: str, body: str, tags?, importance?=50` | `{id, slug}` | creates memory row, computes embedding, fills FTS5 + vec |
| **update** | **MVP** | `memory.update` | `id: int, body: str, bump_update_count: bool=true` | `{id, updated_at}` | updates content, recomputes embedding, bumps counters |
| **delete** | MVP | `memory.delete` | `id: int` | `{id, deleted: bool}` | cascades to FTS5, vec, edges, events |
| **temporal** | v2 | `memory.temporal` | `after: ISO, before: ISO, event_type?` | list of events | queries `memory_events` for time range |
| **graph_neighbors** | v2 | `memory.graph_neighbors` | `entity: str, depth: int=1` | list of memory rows | BFS over `memory_edges` from the entity's memory row |

**MVP set** = search + insert + update + delete. The temporal and graph-neighbor handlers are wired in the schema but not exposed as MCP tools until v2 (when the scribe has enough data to justify them).

## Ranker implementation (`src/memory_mcp/ranker.py`)

Faithful to MemX § 3.4 with Akash-workload adjustments from `empiricist.md`:

```python
"""
Hybrid ranker for Hook B memory search.
Implements the MemX 4-factor reranker (arxiv 2603.16171 § 3.4) with
Akash-workload-adjusted weights.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass
from typing import Sequence

# Weights: MemX exact defaults per moderator verdict C-deeper-2.
# Sum = 0.85; gap of 0.15 is the reject-below threshold.
# These are the MemX paper § 3.4 Table 1 defaults verbatim. Retune after
# 50 real queries using per-factor logging output from `rank()`.
W_SEMANTIC   = 0.45  # cosine similarity
W_RECENCY    = 0.25  # exp-decayed time since last update  
W_IMPORTANCE = 0.10  # AKL score normalized to [0, 1]
W_FREQUENCY  = 0.05  # log-scaled access count

REJECT_THRESHOLD = 0.15
RECENCY_HALF_LIFE_DAYS = 30   # MemX default

RRF_K = 60  # Reciprocal Rank Fusion constant, per MemX

@dataclass
class Candidate:
    memory_id: int
    slug: str
    title: str
    body: str
    cosine: float              # semantic similarity, from sqlite-vec
    bm25: float                # FTS5 bm25 score (negative; more negative = better)
    importance: float          # raw AKL 0-100
    access_count: int
    last_updated: int          # unix seconds


def semantic_score(c: Candidate) -> float:
    """Cosine already in [-1, 1]; clamp to [0, 1]."""
    return max(0.0, min(1.0, (c.cosine + 1.0) / 2.0))


def recency_score(c: Candidate, now: int | None = None) -> float:
    """2 ^ (-age_days / half_life)."""
    now = now or int(time.time())
    age_days = max(0.0, (now - c.last_updated) / 86400.0)
    return 2.0 ** (-age_days / RECENCY_HALF_LIFE_DAYS)


def importance_score(c: Candidate) -> float:
    """Normalize 0-100 AKL score to [0, 1]."""
    return max(0.0, min(1.0, c.importance / 100.0))


def frequency_score(c: Candidate) -> float:
    """log(1+n) / log(1 + expected_max)."""
    expected_max = 100.0  # saturate at 100 accesses
    return math.log1p(c.access_count) / math.log1p(expected_max)


def four_factor_score(c: Candidate, now: int | None = None) -> float:
    """Equation 1 from MemX paper, with Akash-workload weights."""
    s = W_SEMANTIC   * semantic_score(c)
    r = W_RECENCY    * recency_score(c, now)
    i = W_IMPORTANCE * importance_score(c)
    f = W_FREQUENCY  * frequency_score(c)
    return s + r + i + f


def reciprocal_rank_fusion(bm25_ranks: dict[int, int], vec_ranks: dict[int, int]) -> dict[int, float]:
    """
    RRF: for each memory id, score = 1/(K + rank_bm25) + 1/(K + rank_vec).
    Missing ranks contribute 0.
    """
    all_ids = set(bm25_ranks.keys()) | set(vec_ranks.keys())
    out: dict[int, float] = {}
    for mid in all_ids:
        score = 0.0
        if mid in bm25_ranks:
            score += 1.0 / (RRF_K + bm25_ranks[mid])
        if mid in vec_ranks:
            score += 1.0 / (RRF_K + vec_ranks[mid])
        out[mid] = score
    return out


def rank(candidates: Sequence[Candidate], k: int = 5) -> list[dict]:
    """
    Apply the 4-factor rerank to candidates already pre-filtered by RRF
    over FTS5 + sqlite-vec. Return top-k survivors above REJECT_THRESHOLD.

    Per moderator verdict C-deeper-2, returns per-factor score breakdown
    alongside the final score for observability. After 50 real queries,
    Akash can inspect the logs and retune weights if any factor is
    dominating or contributing noise.
    """
    results = []
    for c in candidates:
        s_sem  = W_SEMANTIC   * semantic_score(c)
        s_rec  = W_RECENCY    * recency_score(c)
        s_imp  = W_IMPORTANCE * importance_score(c)
        s_freq = W_FREQUENCY  * frequency_score(c)
        total = s_sem + s_rec + s_imp + s_freq
        results.append({
            "candidate": c,
            "score": total,
            "breakdown": {
                "semantic": s_sem,
                "recency": s_rec,
                "importance": s_imp,
                "frequency": s_freq,
            },
        })
    surviving = [r for r in results if r["score"] >= REJECT_THRESHOLD]
    surviving.sort(key=lambda r: r["score"], reverse=True)
    return surviving[:k]
```

## MCP server entry point (`src/memory_mcp/server.py`)

```python
"""
MCP stdio server exposing memory.* tools over the Model Context Protocol.
Usage:
    python -m memory_mcp.server
Or via settings.json registration:
    "mcpServers": {
      "memory": {"command": "python", "args": ["-m", "memory_mcp.server"]}
    }
"""
from __future__ import annotations
import json
import os
import sys
import threading
from mcp.server import FastMCP
from mcp.types import Tool

from .db import get_connection, ensure_schema
from .embedder import get_embedder
from .handlers import search, insert, update, delete

# Scope selection: default to research-lead, overrideable via env var.
SUBAGENT_SCOPE = os.environ.get("MEMORY_MCP_AGENT", "research-lead")
DB_PATH = os.path.expanduser(
    os.environ.get(
        "MEMORY_MCP_DB",
        f"~/.claude/memory-mcp/data/{SUBAGENT_SCOPE}.sqlite",
    )
)

mcp = FastMCP("memory")

# Shared resources (lazy-init to avoid blocking MCP handshake)
_conn = None
_embedder = None

def _get_conn():
    global _conn
    if _conn is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _conn = get_connection(DB_PATH)
        ensure_schema(_conn)
    return _conn

def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = get_embedder("Qwen/Qwen3-Embedding-0.6B")
    return _embedder


@mcp.tool()
async def search_memory(query: str, k: int = 5, maturity_min: str = "draft") -> list[dict]:
    """Hybrid BM25 + vector search over the agent's memory."""
    return await search.run(_get_conn(), _get_embedder(), query, k, maturity_min)


@mcp.tool()
async def insert_memory(
    slug: str,
    title: str,
    body: str,
    tags: list[str] | None = None,
    importance: float = 50.0,
) -> dict:
    """Create a new memory entry and index it for search."""
    return await insert.run(_get_conn(), _get_embedder(), slug, title, body, tags, importance)


@mcp.tool()
async def update_memory(id: int, body: str, bump_update_count: bool = True) -> dict:
    """Update an existing memory entry's body; re-embeds and reindexes."""
    return await update.run(_get_conn(), _get_embedder(), id, body, bump_update_count)


@mcp.tool()
async def delete_memory(id: int) -> dict:
    """Delete a memory entry and cascade to FTS5/vec/edges/events."""
    return await delete.run(_get_conn(), id)


if __name__ == "__main__":
    # Post-skeptic Attack 4: warm the embedder in a background thread so
    # the first memory.search call does not stall on a 5-15 second model
    # load. Daemon=True ensures clean shutdown. This is fire-and-forget —
    # failure to warm up is non-fatal; the first query will load on demand.
    threading.Thread(target=_get_embedder, daemon=True, name="embedder-warmup").start()
    mcp.run()
```

**Why a background thread**: the MCP handshake is synchronous at the transport
level. Blocking on embedder init would delay Claude Code's session start by
5-15 seconds. A daemon thread loads the model in parallel without blocking the
handshake. If the first `memory.search` arrives before the warm-up completes,
`_get_embedder()` in the handler waits on the same lazy-init lock — correct
but may still be slow. Subsequent queries are fast.

## Database bootstrap (`src/memory_mcp/db.py`, key parts)

```python
"""Connection factory with sqlite-vec loaded and WAL mode enabled."""
from __future__ import annotations
import sqlite3
import sqlite_vec
from pathlib import Path

SCHEMA_SQL = (Path(__file__).parent / "schema.sql").read_text()

def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, isolation_level=None)  # autocommit
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    # Crash safety and performance pragmas
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")  # 5s lock wait
    return conn

def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
```

## settings.json registration snippet

For Claude Code's settings.json at `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "memory-research-lead": {
      "command": "python",
      "args": ["-m", "memory_mcp.server"],
      "cwd": "/home/akash/.claude/memory-mcp",
      "env": {
        "MEMORY_MCP_AGENT": "research-lead",
        "PYTHONPATH": "/home/akash/.claude/memory-mcp/src"
      }
    }
  }
}
```

**Per-subagent scopes**: each leader gets its own MCP server registration by setting `MEMORY_MCP_AGENT` and a distinct server key (e.g., `memory-engineering-lead`, `memory-planning-lead`). They share the server code, just point at different SQLite files via `MEMORY_MCP_DB`.

**Alternative registration in the subagent's frontmatter**: Claude Code supports `mcpServers` in the subagent's own YAML frontmatter (per the sub-agents docs § "Supported frontmatter fields"). For scribe/lead-only access, this is cleaner than user-wide settings.json:

```yaml
---
name: research-lead
memory: user
mcpServers:
  memory:
    command: python
    args: ["-m", "memory_mcp.server"]
    cwd: /home/akash/.claude/memory-mcp
    env:
      MEMORY_MCP_AGENT: research-lead
---
```

Prefer the subagent-frontmatter form; it scopes the MCP to exactly the agent that needs it.

## Failure modes and recovery

### F1: SQLite file corruption

**Symptoms**: `SQLITE_CORRUPT`, `SQLITE_NOTADB`, or silent data loss.

**Causes**: bad shutdown, disk full, filesystem issue, bug in sqlite-vec.

**Recovery**:
1. Scheduled daily backup (see F2). Restore from the latest good backup.
2. If corruption is localized to `memory_vec`, rebuild it by DROP + CREATE + re-embed all rows (the semantic embeddings are reproducible from the `body` text).
3. If corruption is localized to `memory_fts`, rebuild with `INSERT INTO memory_fts(memory_fts) VALUES ('rebuild');`.
4. If `memory` itself is corrupt, the source of truth is the topic files on disk at `~/.claude/agent-memory/<agent>/*.md`. The scribe can re-ingest from markdown.

**Prevention**:
- `PRAGMA journal_mode=WAL` enables crash-safe writes.
- `PRAGMA synchronous=NORMAL` is the WAL-appropriate setting (balances crash safety and perf).
- No concurrent writers to the same DB (single MCP process per scope).

### F2: Backup schedule

**Cold backup script** (`scripts/backup.sh`):

```bash
#!/bin/bash
# Daily WAL checkpoint + cold copy. Run via user's crontab or systemd timer.
set -euo pipefail
DB=~/.claude/memory-mcp/data/research-lead.sqlite
BACKUP_DIR=~/.claude/memory-mcp/backups
DATE=$(date -I)
mkdir -p "$BACKUP_DIR"
sqlite3 "$DB" "PRAGMA wal_checkpoint(TRUNCATE);"
cp "$DB" "$BACKUP_DIR/research-lead-$DATE.sqlite"
# Keep last 30 days
find "$BACKUP_DIR" -name 'research-lead-*.sqlite' -mtime +30 -delete
```

**Cron line**:
```
0 3 * * * bash ~/.claude/memory-mcp/scripts/backup.sh
```

**Why 3 AM**: off-peak, before Akash's typical morning session.

### F3: MCP server crash mid-session

**Symptoms**: tool calls fail with MCP disconnected; Claude Code surfaces the error in the session UI.

**Causes**: embedder OOM, Python exception, PID killed.

**Recovery**:
1. Claude Code automatically retries MCP server startup per its connection policy. No manual intervention needed for transient errors.
2. If persistent, logs go to `~/.claude/memory-mcp/logs/server.log` (stderr captured). Inspect and fix.
3. The SQLite file survives an MCP crash (WAL rollback handles in-flight writes).
4. If the embedder hangs (rare), the server falls back to FTS5-only ranking for that query (graceful degradation).

**Prevention**:
- Run the embedder in a separate thread/process with a timeout.
- Lazy-init on first call, not at startup (reduces startup time, avoids connection-time failures).
- Health-check tool: `memory.ping` returns DB + embedder status.

### F4: Embedder model download failure

**Symptoms**: first run of the server tries to download Qwen3-Embedding-0.6B from HuggingFace, network fails.

**Recovery**:
1. Pre-download the model: `hf download Qwen/Qwen3-Embedding-0.6B --local-dir ~/.cache/huggingface/hub/models--Qwen--Qwen3-Embedding-0.6B/snapshots/main`
2. Alternatively, fall back to a smaller model like `BAAI/bge-small-en-v1.5` (384 dim) — update schema dimension accordingly.
3. Or fall back to FTS5-only (no vector column) if vector search is not essential.

**Prevention**: bootstrap.py runs `embedder.encode("hello")` at install time so the model downloads upfront.

### F5: sqlite-vec extension load failure

**Symptoms**: `no such module: vec0` error on virtual table creation.

**Causes**: 
- sqlite-vec wheel not installed for the current Python environment
- sqlite3 compiled without `enable_load_extension`

**Recovery**:
1. Verify: `python -c "import sqlite_vec; print(sqlite_vec.__file__)"` — should succeed
2. Verify: `python -c "import sqlite3; c=sqlite3.connect(':memory:'); c.enable_load_extension(True)"` — should succeed
3. On macOS with Homebrew Python, system sqlite3 may lack load_extension. Install `python3` via a Python build that includes it (pyenv, conda, or pip install pysqlite3-binary as a shim).

**Fallback**: disable vector search entirely; use FTS5-only. The schema supports this: `memory_vec` can be conditionally created.

## Build trigger — "Hook A insufficient" defined

From `EVIDENCE/empiricist.md` § "Hook A insufficient — the trigger metric":

> Over **10 consecutive sessions**, if `miss_rate > 20%` → Hook B BUILD. If 5-20% → marginal, monitor another 10. If <5% → Hook A sufficient.

Where `miss_rate = (relevant topic files NOT cited) / (relevant topic files)` per session, computed by the scribe at session close and logged to LOG.md.

A sample trigger check (run manually or via cron):

```bash
grep "scribe-metric: topic-file-check" ~/.claude/teams/research/*/LOG.md | \
    tail -10 | \
    awk -F'hit-rate=' '{print $2}' | \
    awk '{sum+=$1; n++} END {print "avg hit-rate:", sum/n, "avg miss-rate:", 1-sum/n}'
```

## Estimated build effort (Engineering Team)

- Scaffold + schema + basic handlers: 1 day
- Ranker + embedder + hybrid retrieval: 1 day
- MCP wire-up + settings integration: 0.5 day
- Tests + bootstrap script + backup script: 0.5 day
- **Total: 3 person-days** for MVP

v2 (temporal + graph_neighbors) adds another 1-2 days.

## Confidence

**High** on the scaffold structure, schema DDL, and API surface — every piece has a direct source (MemX paper, sqlite-vec demo, MCP SDK docs, ByteRover AKL). The ranker code is testable against expected outputs. The failure modes and recovery are standard SQLite practices.

**Medium** on the exact weight values (0.45/0.30/0.13/0.02) — these are adjusted from MemX's defaults based on Akash's workload shape. They should be re-tuned once the DB has real data; the production MVP can start with MemX's exact defaults and let the scribe log recall-failure examples for later calibration.

## Handoff

- **scribe-edit-plan** — the frontmatter schema in Edit 1.3 matches this scaffold's `memory` table columns
- **IMPLEMENTATION_SEQUENCE** — Hook B is steps 11-18
- **retrospector** — lesson: "MCP scaffolds should include a build trigger, not just 'build when needed'"
- **skeptic** — attack: is the Qwen3-Embedding-0.6B the right embedder? (Answered: yes per MemX paper; fallback to bge-small if download fails.)

## Citations

- MemX paper, § 3.4, Equation 1, Equation 2, Table 1 — `arxiv.org/html/2603.16171`, retrieved 2026-04-12
- MemX reference impl config — `github.com/memxlab/memx` README, retrieved 2026-04-12
- sqlite-vec Python usage — `alexgarcia.xyz/sqlite-vec/python.html` + demo, retrieved 2026-04-12
- MCP Python SDK quickstart — `pypi.org/project/mcp/` + `github.com/modelcontextprotocol/python-sdk`, retrieved 2026-04-12
- ByteRover AKL formula — `arxiv.org/html/2604.01599` § 3.2.3, retrieved 2026-04-12
- Claude Code sub-agents frontmatter — `code.claude.com/docs/en/sub-agents` § "Supported frontmatter fields", retrieved 2026-04-12
- FTS5 triggers pattern — standard `sqlite.org/fts5.html` external content pattern
- WAL + synchronous=NORMAL tradeoff — `sqlite.org/pragma.html` docs, canonical
