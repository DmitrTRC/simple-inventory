create table if not exists Users
(
    id       INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email    TEXT NOT NULL,
    age      INTEGER
)

