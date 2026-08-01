CREATE TABLE IF NOT EXISTS rankings (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    position INTEGER NOT NULL CHECK (position >= 1),
    url TEXT NOT NULL
);

