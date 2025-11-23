-- Initialize MariaDB database
CREATE DATABASE IF NOT EXISTS scientific_articles;
USE scientific_articles;

-- Create articles table
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INT,
    abstract TEXT,
    arxiv_id VARCHAR(50),
    url TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions to app user
GRANT ALL PRIVILEGES ON scientific_articles.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

SELECT 'MariaDB database initialized successfully' as status;