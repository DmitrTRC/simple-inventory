create table if not exists todos
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    task           TEXT NOT NULL,
    category       TEXT CHECK (category IN ('BACKLOG', 'MAINTENANCE', 'BIRTHDAY', 'READING', 'WATCHING',
                                            'SHOPPING'))     DEFAULT 'BACKLOG',
    date_added     TEXT NOT NULL,
    date_completed TEXT,
    status         TEXT CHECK (status IN ('UNDONE', 'DONE')) DEFAULT 'UNDONE'
)
