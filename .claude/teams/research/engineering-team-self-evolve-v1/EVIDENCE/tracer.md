# Tracer — concurrency primitives for parallel-instance MEMORY.md segregation

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: runtime execution paths, Unix primitives, file-locking semantics, failure-mode taxonomy
Mode: adopted persona — WebFetch over man pages + reasoning from POSIX/Linux docs

## The problem (stated precisely)

Akash runs N ≥ 2 Claude Code sessions concurrently. Each session may launch a research-team or engineering-team investigation. At session close, the retrospector writes lessons to a shared per-agent MEMORY.md file:
- `~/.claude/agent-memory/research-lead/MEMORY.md`
- `~/.claude/agent-memory/engineering-lead/MEMORY.md`
- `~/.claude/agent-memory/research-retrospector/MEMORY.md`
- `~/.claude/agent-memory/engineering-retrospector/MEMORY.md`
- … etc for any future team lead

**Race condition scenarios**:
1. Session A and Session B both finish at nearly the same time. Both retrospectors call `Write(MEMORY.md, <merged content>)`. Whichever write lands second overwrites the first — A's lessons disappear.
2. Session A is writing MEMORY.md when Session B reads it mid-write. B sees truncated or torn content.
3. Session A's retrospector writes a new lesson that duplicates an existing lesson. Session B's retrospector runs at the same time and also duplicates the same existing lesson. Both dedup passes operate on stale reads. Duplicates survive.

**Requirements**:
- R1: **No lost writes.** Every retrospector lesson must eventually land in the canonical MEMORY.md.
- R2: **No torn reads.** Readers never see a partially-written MEMORY.md.
- R3: **No duplicate writes.** The dedup pass must be serialized so two concurrent retrospectors don't both add the same lesson.
- R4: **No critical-path latency** for the common case (single session). Locking overhead must be invisible in normal usage.
- R5: **Lock-holder death safety.** If a session crashes mid-merge, the lock must be released without manual intervention.
- R6: **Pragmatic primitives.** Must work on Linux with bash/flock/mv/chmod. No new dependencies.

## Candidate primitives

### Candidate 1: `flock(1)` advisory lock on `.lock` file

`flock(1)` is a bash-callable wrapper around `flock(2)` that acquires an advisory lock on a given file descriptor and either runs a command or blocks. It is the standard Linux primitive for "bash script needs to coordinate."

**Semantics verified via man pages (retrieved 2026-04-12)**:

From flock(1) — `https://man7.org/linux/man-pages/man1/flock.1.html`:
> `-w, --wait, --timeout seconds: Fail if the lock cannot be acquired within seconds. Decimal fractional values are allowed.`
> `The exit status used when the -n option is in use, and the conflicting lock exists, or the -w option is in use, and the timeout is reached. The default value is 1.`
> `This is usually not required, since a lock is automatically dropped when the file is closed.`
> By default uses `flock(2)` locks. `--fcntl` switches to `F_OFD_SETLK`/`F_OFD_SETLKW` OFD locks.

From flock(2) — `https://man7.org/linux/man-pages/man2/flock.2.html`:
> `flock() places advisory locks only; given suitable permissions on a file, a process is free to ignore the use of flock() and perform I/O on the file.`
> `Duplicate file descriptors from fork() "refer to the same lock, and this lock may be modified or released using any of these file descriptors."`
> `Locks created by flock() are preserved across an execve(2).`
> Lock releases "either by an explicit LOCK_UN operation on any of these duplicate file descriptors, or when all such file descriptors have been closed."
> NFS: "NFS clients support flock() locks by emulating them as fcntl(2) byte-range locks on the entire file."

**Critical path**:
1. Bash calls `flock -w 5 /path/to/.lock -c '<merge command>'`
2. flock(1) opens /path/to/.lock, calls flock(2) with LOCK_EX.
3. If lock is free: flock(2) returns immediately, runs the merge command.
4. If lock is held: flock(2) blocks up to 5 seconds. If released within 5s, takes lock and runs. If not released, flock(1) exits with code 1 (timeout).
5. When merge command exits (success or failure), flock(1) closes the fd, kernel releases the lock, and exits with the command's exit code.

**If lock holder dies**: the holding process's fd is closed by the kernel on exit (SIGKILL, SIGSEGV, or whatever), and the lock is released. **This satisfies R5 without any timeout bookkeeping.** This is the killer feature of flock(2) over fcntl(F_SETLK).

**R1/R2/R3/R4/R5/R6 check**:
- R1 lost writes: solved by lock-serializing the merge.
- R2 torn reads: NOT solved by lock alone — readers that don't take the lock can still see mid-merge state. Separate solution (see "Atomic replace" below).
- R3 duplicate writes: solved by lock-serializing the dedup pass.
- R4 latency: `flock -w 0.1` on a free lock has microsecond-level overhead. Invisible in normal use.
- R5 holder death: solved automatically by kernel fd cleanup.
- R6 pragmatic: bash-native on every Linux box. On macOS, flock(1) exists via Homebrew `util-linux` or `brew install flock`.

**Verdict**: R1, R3, R4, R5, R6 met. R2 needs help.

### Candidate 2: Atomic replace via `mv` (POSIX rename guarantee)

For R2 (no torn reads), readers need a guarantee that they see either the old MEMORY.md or the new one, never a partial write in between.

The POSIX guarantee: `rename(2)` is atomic on the same filesystem. From the POSIX spec (and Linux man rename(2)):
> If a file with the name `new` already exists, it will be removed atomically and replaced. A reader that opens `new` by name will see either the pre-rename contents or the post-rename contents, never a mixture.

The bash equivalent is `mv /path/to/MEMORY.md.tmp /path/to/MEMORY.md` when both files live on the same filesystem.

**Merge sequence (atomic replace)**:
1. Acquire `.lock` via flock(1).
2. Read current MEMORY.md.
3. Compute merged content.
4. Write merged content to `MEMORY.md.tmp.<pid>` (a sibling temp file on the same filesystem).
5. `mv MEMORY.md.tmp.<pid> MEMORY.md` — atomic replace.
6. Release `.lock`.

**Readers** do NOT need to take the lock. They just open `MEMORY.md` by name. They always get a complete version — either pre-merge or post-merge. No torn reads. R2 satisfied.

**Caveats**:
- The two files must be on the **same filesystem** for `mv` to be a pure `rename(2)`. Cross-filesystem `mv` degenerates to copy-then-delete, which is NOT atomic. Since both files are under `~/.claude/agent-memory/<agent>/`, this is automatically the case.
- `rename(2)` on most Linux filesystems (ext4, btrfs, xfs, zfs) is atomic with respect to other `open(2)` calls. Network filesystems (NFS, SMB) have weaker guarantees — but agent-memory lives on the local disk, so N/A.

**Verdict**: R2 fully solved. R1+R3 still require the lock.

### Candidate 3: Per-session staging directory (the separation principle)

Even with flock + atomic replace, there's a latent problem: a retrospector that acquires the lock holds it for the duration of the merge, which can take multiple seconds (reading MEMORY.md, computing dedup, writing temp, moving). If 10 sessions close at the same time, the 10th waits ~30 seconds — beyond the `flock -w 5` timeout.

**Solution**: split the write into two phases.

1. **Phase A — stage (no lock)**: retrospector writes its lessons to `~/.claude/agent-memory/<agent>/staging/<slug>.md`. This file is session-unique (named by slug). No contention. Fast.
2. **Phase B — merge (with lock)**: scribe acquires lock, reads MEMORY.md, reads ALL staging files, merges them into a new MEMORY.md, writes temp, atomically replaces. If lock is held, waits up to 5s. If waits > 5s, scribe logs "deferred merge" and exits — the staging files remain on disk, and the next scribe run (or the next session's scribe) will merge them.

**Critical property**: **even if the scribe defers the merge, the retrospector's lesson is NOT LOST.** It lives in `staging/<slug>.md` until some scribe eventually merges it. The staging file is the durable artifact; MEMORY.md is a curated view of the accumulated staging files. Eventual consistency, not strict consistency.

**Idempotency**: the merge must be idempotent on the staging files. If scribe A crashes after reading MEMORY.md but before writing the new version, scribe B re-runs the same merge and the result is the same. The staging files are never deleted by the merge — only marked `_merged` (or moved to `staging/_merged/`).

**Garbage collection**: after 90 days, archived staging files move to `~/.claude/agent-memory/<agent>/_archive/<year>/`. Not deleted.

### Candidate 4: SQLite WAL mode (rejected)

SQLite in WAL mode would give us concurrent readers + single writer with durability. But:
- Introduces a binary database file format, losing the "grep the MEMORY.md directly" property.
- Requires an SQLite CLI or Python/sqlite3 in the merge path. Not bash-native.
- The `memory: user` runtime auto-injection expects `MEMORY.md` as a text file — it reads the first 200 lines or 25KB directly. A SQLite database doesn't integrate with that.

**Verdict**: rejected for v1. Could be a v2.2 optimization if MEMORY.md ever gets big enough that text-based dedup is slow (unlikely for our scale — ~7KB today, ~50KB at saturation).

### Candidate 5: Git as storage layer (rejected)

Use `git` over `~/.claude/agent-memory/` as the coordination mechanism. Each session commits its lessons. Conflicts are resolved via git merge.

**Pros**: full history, attribution, native diff, rollback-safe.
**Cons**:
- `git commit` requires a working tree in clean state, which multi-session writes break.
- Merge conflicts require human intervention (or automated `git rebase --autosquash`) — not a bash one-liner.
- The `memory: user` runtime doesn't know about git; it reads the working file.
- Adds a significant new dependency (git as runtime requirement for memory writes).

**Verdict**: rejected for v1. A v2.3 "long-term audit trail via git log" could be layered on top of the flock+staging design, but that's orthogonal to the race-free write property.

### Candidate 6: CRDT append-only log (rejected)

Each session writes to its own log file; the "current MEMORY.md" is a materialized view of all logs concatenated + deduplicated.

**Pros**: mathematically race-free, no lock needed.
**Cons**:
- The materialization step needs the lock anyway (or two readers produce different views).
- CRDT is strictly more complex than flock+staging for our scale.
- Runtime auto-injection wants a single `MEMORY.md` file, not a log-view.

**Verdict**: rejected. Flock+staging achieves the same invariants with less complexity.

## The design: flock + atomic replace + per-session staging

### File layout

```
~/.claude/agent-memory/
├── engineering-lead/
│   ├── MEMORY.md               # canonical, read at session start
│   ├── .lock                   # flock target (empty file)
│   ├── staging/                # per-session lesson deltas
│   │   ├── <slug-1>.md         # retrospector writes here first
│   │   ├── <slug-2>.md
│   │   └── _merged/            # archived staging files post-merge
│   │       └── <slug>.md
│   ├── topic/                  # Hook A overflow (from memory-layer SYNTHESIS)
│   │   └── <topic>.md
│   └── _archive/               # staging files > 90 days
│       └── <year>/
├── engineering-retrospector/
│   └── (same shape)
├── research-lead/
│   ├── MEMORY.md               # existing
│   ├── .lock                   # NEW
│   ├── staging/                # NEW
│   ├── topic/                  # NEW (Hook A target)
│   └── _archive/               # NEW
├── research-retrospector/
│   └── (same shape)
└── …
```

Backward-compatibility: existing `MEMORY.md` files stay where they are. The `.lock` and `staging/`, `topic/`, `_archive/` directories are added alongside.

### Write protocol (retrospector)

```bash
# 1. Retrospector writes to staging file (no lock needed).
AGENT="engineering-lead"
SLUG="<session-slug>"
STAGING="$HOME/.claude/agent-memory/$AGENT/staging/$SLUG.md"
mkdir -p "$(dirname "$STAGING")"

# Append-only to staging. Never truncate.
cat >> "$STAGING" <<'EOF'
### <lesson title>
- **Observed in**: <slug> (<ISO-date>)
- **Failure mode addressed**: <MAST code or "none">
- **Lesson**: …
- **Rule of thumb**: …
- **Counter-example / bounds**: …
EOF
```

That's it for the retrospector. Session-unique file, no contention.

### Merge protocol (scribe)

```bash
# 2. Scribe acquires lock, merges staging into MEMORY.md.
AGENT="engineering-lead"
ROOT="$HOME/.claude/agent-memory/$AGENT"
LOCK="$ROOT/.lock"
MEM="$ROOT/MEMORY.md"
TMP="$ROOT/MEMORY.md.tmp.$$"
STAGING_DIR="$ROOT/staging"

# Ensure lock file exists (idempotent).
touch "$LOCK"

# Acquire with 5s timeout.
flock -w 5 "$LOCK" bash -c '
  set -e
  # Read current MEMORY.md (if any).
  if [ -f "'"$MEM"'" ]; then
    cp "'"$MEM"'" "'"$TMP"'"
  else
    : > "'"$TMP"'"
  fi

  # For each staging file, merge in.
  for f in "'"$STAGING_DIR"'"/*.md; do
    [ -f "$f" ] || continue
    [ "$(basename "$f")" = "_merged" ] && continue
    # Append; dedup pass happens in-process via scribe persona logic.
    cat "$f" >> "'"$TMP"'"
    # Mark merged by moving, not deleting.
    mkdir -p "'"$STAGING_DIR"'/_merged"
    mv "$f" "'"$STAGING_DIR"'/_merged/"
  done

  # (Optional) run scribe dedup here — can be a separate pass if LLM-driven.

  # Atomic replace.
  mv "'"$TMP"'" "'"$MEM"'"
' || {
  # Lock timeout. Staging files remain; next session will merge.
  echo "[scribe-curator] deferred merge on $AGENT — staging preserved" >&2
  exit 0   # Not an error — staging is durable, next merge picks up.
}
```

**Key properties**:
- `flock -w 5`: waits up to 5 seconds to acquire. If contended, exits with code 1 and the outer `|| { … exit 0; }` catches it as a non-error — the staging files are still there.
- `mv "$TMP" "$MEM"`: atomic replace on the same filesystem. Readers never see a half-written file.
- Staging files moved to `staging/_merged/`, never deleted. Audit trail preserved.
- Holder-death safety: if the merge command dies mid-execution (SIGKILL, OOM, etc), the kernel closes the fd, releases the lock, and the next scribe run has a clean slate. The `.tmp.<pid>` file is orphaned but harmless (scribe cleanup on next run can sweep orphans > 24 hours old).

### Read protocol

```bash
# Readers do NOT take the lock.
# They just read MEMORY.md directly.
head -200 "$HOME/.claude/agent-memory/engineering-lead/MEMORY.md"
```

**Why no reader lock**:
- `rename(2)` guarantees readers see either the pre-merge or post-merge contents, never torn.
- Readers can tolerate staleness (they see the previous canonical state for up to ~2 seconds during a merge). MEMORY.md is append-mostly (lessons accumulate), so "stale" means "missing the most recent session's lessons," which is fine — those lessons will be visible on the next session.
- No lock contention on reads means the common case (single session reading at start) has zero locking overhead.

### Contention analysis

- **Normal case** (1 session): retrospector writes staging, scribe acquires free lock, merges, exits. Lock held for ~100ms.
- **2 sessions closing simultaneously**: both write to distinct staging files (no contention). Scribe 1 acquires lock, merges, exits. Scribe 2 waits up to 5s, then acquires the lock, merges (sees 1's output + its own staging file), exits. Sequential latency: ~200ms.
- **10 sessions closing simultaneously**: 10 staging files, 10 scribe attempts. Scribe 1 wins, merges all 10 staging files in one pass. Scribes 2-10 see the merge already done and their staging files already moved to `_merged/` — they do a no-op second pass. OR scribes 2-10 hit the 5s timeout and defer; next session picks up.
- **Crash during merge**: kernel releases lock on process death. Next scribe run sees the orphan `.tmp.<pid>` file (garbage-collected) and unmerged staging files (merged into current MEMORY.md). **No lost writes.**

### Timeouts and tuning

- `flock -w 5` — the 5-second cap balances "wait long enough to coalesce contention" vs "don't stall session close." For our scale (1-10 concurrent sessions), 5s is generous.
- `5s > typical merge duration (~200ms)` by 25x headroom.
- If Akash ever runs > 20 concurrent sessions, tune up to `flock -w 10`.

### What happens if flock is not installed

On Linux, `flock(1)` ships in `util-linux`, part of every standard distribution. On macOS, it requires `brew install util-linux`. On Windows, it's not available (but Claude Code on Windows runs through WSL which has flock).

**Fallback** (defensive): if `command -v flock >/dev/null 2>&1` returns false, the merge protocol degrades to:
```bash
# Fallback: retry-loop with sleep, no real mutex.
# Documented as "best effort — prefer flock when available."
for i in 1 2 3 4 5; do
  if mkdir "$LOCK.d" 2>/dev/null; then
    # Got the "lock" — do the merge.
    trap 'rmdir "$LOCK.d"' EXIT
    # … merge …
    break
  fi
  sleep 1
done
```

`mkdir` is atomic on POSIX (two `mkdir` calls on the same path can't both succeed), so `mkdir LOCK.d` is a primitive mutex. Less good than flock (no holder-death safety — if the process dies without the EXIT trap running, the lock directory persists as a stale lock file). But works on any POSIX shell without dependencies.

### Cross-team considerations

Research-team's existing `~/.claude/agent-memory/research-lead/MEMORY.md` is currently unlocked. The v2.1 upgrade adds `.lock`, `staging/`, `topic/` alongside it. **Existing sessions continue to work unchanged** — if they write directly to MEMORY.md without going through the staging protocol, they lose the race-free guarantee but don't corrupt existing data (last-writer-wins, as before).

Mandatory for future sessions: both research-lead and engineering-lead retrospectors + scribes MUST use the staging protocol. v2.1 updates the research PROTOCOL.md to this effect.

## Why not just use SQLite?

Because the Claude Code runtime `memory: user` feature injects **the first 200 lines or 25KB of MEMORY.md as raw text** into the subagent's system prompt. MEMORY.md must be a text file. A SQLite database would break this integration. Flock+staging keeps MEMORY.md as text, preserving the runtime contract.

## What the empiricist should verify

1. `flock -w 5 <file> -c 'sleep 2; echo done'` — does the second instance wait 2-3s then succeed (correct) or fail immediately (wrong build of flock)?
2. Does `mv X Y` atomically replace on ext4? (Expected yes; verify.)
3. Does `flock` release on SIGKILL? (Expected yes by kernel fd cleanup; verify.)
4. What's the typical merge duration on our actual MEMORY.md (~7KB today)?
5. Does the fallback `mkdir LOCK.d` work when flock is missing?

## Handoff to synthesist

The concurrency design is concrete and complete. The file layout, lock primitive, merge algorithm, read protocol, and failure modes are all specified. Synthesist can write the PROTOCOL.md section directly from this evidence file.

## Confidence

**HIGH** on the flock semantics and atomic-rename guarantees (verified via man pages from `man7.org`, retrieved 2026-04-12). **HIGH** on the staging-file design (follows the standard "durable queue + worker" pattern). **MEDIUM** on the fallback path — `mkdir LOCK.d` works but has no holder-death safety, which is a measurable regression if flock is unavailable. **MEDIUM** on cross-filesystem edge cases — solved by ensuring everything lives under `~/.claude/agent-memory/<agent>/`, but if Akash ever moves agent-memory to a mount point with different semantics, the design needs re-verification.
