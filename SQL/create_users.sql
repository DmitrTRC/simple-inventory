create table if not exists users
(
    id INTEGER NOT NULL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    phone INTEGER,
    age INTEGER NOT NULL
);
