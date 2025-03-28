create table if not exists todos
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    task           TEXT NOT NULL,
    category       TEXT DEFAULT 'BACKLOG',
    date_added     TEXT NOT NULL,
    date_completed TEXT,
    status         TEXT DEFAULT 'UNDONE'
)
