create table if not exists users
(
    id INTEGER NOT NULL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    phone INTEGER,
    age INTEGER NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0
);
