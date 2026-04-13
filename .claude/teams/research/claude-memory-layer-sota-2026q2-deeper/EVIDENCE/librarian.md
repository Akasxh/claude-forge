# Librarian — MCP SDK, sqlite-vec, and MemX ranker primary sources

Sub-question: gather implementation-grade primary-source detail on (a) the official MCP Python SDK, (b) sqlite-vec's Python usage surface, (c) the exact MemX 4-factor reranking formula with weights and half-life.

## Method

- WebFetched PyPI pages for `mcp` and `sqlite-vec` (both retrieved 2026-04-12)
- WebFetched MemX paper HTML at `arxiv.org/html/2603.16171` (retrieved 2026-04-12)
- WebFetched MemX reference Rust implementation at `github.com/memxlab/memx` (retrieved 2026-04-12)
- WebFetched sqlite-vec's official Python demo at `github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py` (retrieved 2026-04-12)
- WebFetched Claude Code docs for scope-field verification

## MCP Python SDK — version, API surface, minimum Python

From `pypi.org/project/mcp/`, retrieved 2026-04-12:

- **Current version**: **1.27.0**, released 2026-04-02 (10 days before this session — fresh)
- **Minimum Python version**: **>=3.10** (supports 3.10, 3.11, 3.12, 3.13)
- **Transport**: stdio, SSE, Streamable HTTP
- **Decorators exposed by the FastMCP helper**:
  - `@mcp.tool()` — functions that "execute code or otherwise produce a side effect"
  - `@mcp.resource("greeting://{name}")` — templates for "loading information into the LLM's context"
  - `@mcp.prompt()` — templates for reusable LLM interactions
- **Official repository**: `github.com/modelcontextprotocol/python-sdk`

**Implication**: Python MCP SDK is production-grade and recent enough (Apr 2, 2026) to match Akash's 2026-04-12 cutoff. No API churn risk.

## sqlite-vec — version, Python usage, loading pattern

From `pypi.org/project/sqlite-vec/`, retrieved 2026-04-12:

- **Stable version**: **0.1.9**, released 2026-03-31
- **Alphas**: 0.1.10a1, 0.1.10a2, 0.1.10a3 on 2026-04-01 (active development)
- **Python compatibility**: Python 3 (wheels for Windows x86-64, Linux manylinux, macOS Intel + ARM64)
- **Distribution**: wheel (no source distribution); no compile step required on supported platforms
- **License**: dual MIT / Apache 2.0
- **Maintainer**: Alex Garcia (alexgarcia)

### Exact Python loading syntax (verbatim from `alexgarcia.xyz/sqlite-vec/python.html`, retrieved 2026-04-12)

```python
import sqlite3
import sqlite_vec

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)
```

### Virtual table creation (from the official demo `examples/simple-python/demo.py`, retrieved 2026-04-12)

```python
import sqlite3
import sqlite_vec
from typing import List
import struct

def serialize_f32(vector: List[float]) -> bytes:
    """Serialize a list of floats to compact bytes for vec0."""
    return struct.pack(f"{len(vector)}f", *vector)

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

db.execute("CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[4])")

items = [
    (1, [0.1, 0.1, 0.1, 0.1]),
    (2, [0.2, 0.2, 0.2, 0.2]),
]
for rowid, vec in items:
    db.execute(
        "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
        (rowid, serialize_f32(vec)),
    )

rows = db.execute(
    """
    SELECT rowid, distance FROM vec_items
    WHERE embedding MATCH ?
    ORDER BY distance LIMIT 3
    """,
    (serialize_f32([0.3, 0.3, 0.3, 0.3]),),
).fetchall()
```

**Key takeaways for Hook B**:

1. The loading sequence is 4 lines: `enable_load_extension(True)`, `sqlite_vec.load(db)`, `enable_load_extension(False)`, then normal SQL.
2. The virtual table uses `vec0` module with a `float[N]` column spec where N is the embedding dimensionality.
3. Vectors serialize via `struct.pack(f"{n}f", *vector)` — compact binary, not JSON.
4. Query uses `WHERE embedding MATCH ?` with the serialized query vector, then `ORDER BY distance LIMIT k` for top-k.
5. Secondary columns (metadata, text content) can be added via a companion regular table joined on `rowid`.

## MemX 4-factor reranking — exact formula

From MemX paper HTML at `arxiv.org/html/2603.16171`, § 3.4, retrieved 2026-04-12:

**Four factors** (names verbatim from the paper):

1. **Semantic similarity** — `f_sem(m)` — cosine similarity between query embedding and memory embedding
2. **Recency** — `f_rec(m)` — time-decayed score
3. **Frequency** — `f_freq(m)` — access count based
4. **Importance** — `f_imp(m)` — curator-assigned priority

**Combination formula** (Equation 1 verbatim):

```
score(m) = α_s · f_sem(m)  +  α_r · f_rec(m)  +  α_f · f_freq(m)  +  α_i · f_imp(m)
```

**Weight values** (Table 1, defaults in MemX):

| Coefficient | Value | Factor     |
|-------------|-------|------------|
| `α_s`       | 0.45  | semantic   |
| `α_r`       | 0.25  | recency    |
| `α_f`       | 0.05  | frequency  |
| `α_i`       | 0.10  | importance |
| **sum**     | **0.85** | (the remaining 0.15 is a threshold gap; the paper treats scores below 0.15 as rejection) |

**Recency decay formula** (Equation 2 verbatim):

```
f_rec(m) = 2 ^ ( -d_m / h )
```

Where:
- `d_m = (now - t_m) / 86400` — age of memory entry in days
- `h = 30` — default half-life, in days (30-day half-life means the score halves every 30 days)

**Embedding configuration** (§ 5.1):
- Model: **Qwen3-Embedding-0.6B**
- Dimension: **1,024**
- FTS5 tokenizer: `unicode61`

**Benchmark numbers** (verbatim from abstract, retrieved 2026-04-12):
- Hit@1 = **91.3%** on a default scenario
- Hit@1 = **100%** under high confusion (keyword-dense queries)
- End-to-end search latency: **< 90ms**
- FTS5 speedup: **1,100x at 100k records** vs LIKE-based keyword search

**Cross-verification from the reference Rust implementation** at `github.com/memxlab/memx`, retrieved 2026-04-12:

In the reference `README.md`, the four weights are exposed as config keys:

```
semantic_weight = 0.45
recency_weight = 0.25
importance_weight = 0.10
frequency_weight = 0.05
```

These are **commented-out optional overrides** in the config file, suggesting they are the defaults compiled in. Sum = 0.85, matching the paper. The repo has only 2 stars and 2 commits, which is effectively a "reference dump" not a maintained project — the paper is the primary source, not the repo.

## Hook B hybrid ranker implementation recommendation

The Hook B ranker should directly adopt the MemX formula. For Akash's workload the adjustments from the default are:

1. **Keep semantic weight = 0.45**: his workload is vocabulary-rich (research topics, paper titles, agent names). Cosine similarity over a small corpus is his highest-signal factor.
2. **Increase recency to 0.30** (from 0.25): his sessions span weeks; stale verdicts matter less. Half-life stays at 30 days.
3. **Decrease frequency to 0.02** (from 0.05): his corpus is too small (<1000 entries) for frequency to be useful at the low end.
4. **Increase importance to 0.13** (from 0.10): the scribe's "Reinforced by" field is already a priority signal — leverage it.

Adjusted weights sum to 0.90 (tighter threshold than MemX's 0.85). Below 0.10 → reject.

**BM25 integration**: FTS5 returns a BM25 score (negative, more negative = better) via the built-in `bm25(fts)` function. To combine with the vector path, the ranker uses **Reciprocal Rank Fusion (RRF)** per MemX's own pipeline (§ 3.4):

```
rrf(m) = 1/(60 + rank_bm25(m))  +  1/(60 + rank_vec(m))
```

where 60 is the MemX default RRF constant. Then the 4-factor score above is applied to the RRF-surviving top-K.

## Confidence

**High** on the MemX formula: verbatim from paper HTML + cross-verified in the reference repo's commented config defaults. **High** on sqlite-vec and MCP SDK: primary pages from PyPI + official example repo. No paraphrase drift.

## Handoff

- **empiricist** (cost/latency sizing) — the numbers above feed the hook comparison table
- **skeptic** — attack: is the Qwen3-Embedding-0.6B vs a smaller embedding model the right choice for sub-100ms local search?
- **mcp-scaffold** (evidence file for the skeleton code) — uses the loading/query patterns verbatim

## Citations

- MCP Python SDK PyPI page — `pypi.org/project/mcp/`, retrieved 2026-04-12 (version 1.27.0, released 2026-04-02)
- sqlite-vec PyPI — `pypi.org/project/sqlite-vec/`, retrieved 2026-04-12 (0.1.9 stable, 0.1.10 alphas)
- sqlite-vec Python docs — `alexgarcia.xyz/sqlite-vec/python.html`, retrieved 2026-04-12
- sqlite-vec demo — `github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py`, retrieved 2026-04-12
- MemX paper — `arxiv.org/abs/2603.16171`, retrieved 2026-04-12 (full-text HTML § 3.4, § 5.1, Equation 1, Equation 2, Table 1)
- MemX reference repo — `github.com/memxlab/memx`, retrieved 2026-04-12 (2 stars, 2 commits, config defaults)
- Claude Code subagent memory — `code.claude.com/docs/en/sub-agents` § "Enable persistent memory", retrieved 2026-04-12
- Claude Code auto memory — `code.claude.com/docs/en/memory` § "How it works", retrieved 2026-04-12
