CREATE TABLE IF NOT EXISTS news
(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    title_text TEXT NOT NULL,
    wiki_title_raw TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_detail
(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    wiki_tid TEXT NOT NULL,
    summary TEXT,
    description TEXT,
    thumbnail TEXT,
    image TEXT,
    timestamp TIMESTAMP,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    news_id BIGINT NOT NULL,
    CONSTRAINT fk_news FOREIGN KEY (news_id) REFERENCES news (
        id
    ) ON DELETE CASCADE
);
