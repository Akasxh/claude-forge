-- Memory MCP Schema — SQLite + FTS5
-- Core memory entries
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    source_agent TEXT NOT NULL,
    session_slug TEXT,
    lesson_type TEXT DEFAULT 'lesson',
    tags TEXT DEFAULT '',
    importance REAL DEFAULT 50.0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    accessed_at TEXT DEFAULT (datetime('now')),
    access_count INTEGER DEFAULT 0,
    reinforced_count INTEGER DEFAULT 0
);

-- FTS5 full-text search index
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content, source_agent, tags, session_slug,
    content='memories',
    content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content, source_agent, tags, session_slug)
    VALUES (new.id, new.content, new.source_agent, new.tags, new.session_slug);
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content, source_agent, tags, session_slug)
    VALUES ('delete', old.id, old.content, old.source_agent, old.tags, old.session_slug);
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content, source_agent, tags, session_slug)
    VALUES ('delete', old.id, old.content, old.source_agent, old.tags, old.session_slug);
    INSERT INTO memories_fts(rowid, content, source_agent, tags, session_slug)
    VALUES (new.id, new.content, new.source_agent, new.tags, new.session_slug);
END;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(source_agent);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC);
CREATE INDEX IF NOT EXISTS idx_memories_accessed ON memories(accessed_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_lesson_type ON memories(lesson_type);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at DESC);
