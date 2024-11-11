DROP TABLE IF EXISTS headlines;

CREATE TABLE headlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    link TEXT,
    pubDate TEXT,
    descriptionText TEXT,
    newspaper TEXT
);