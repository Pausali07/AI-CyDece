CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_ip TEXT,
    start_time TEXT,
    protocol TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS pcaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    file_size INTEGER,
    ingested_at TEXT,
    source TEXT
);
