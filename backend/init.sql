CREATE TABLE trending_topics (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    popularity INT NOT NULL,
    fetched_at TIMESTAMP NOT NULL
);