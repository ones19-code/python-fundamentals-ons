<<<<<<< HEAD
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
=======
-- Création de la table users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertion de données initiales
INSERT INTO users (username, email) VALUES 
('eva', 'eva@example.com'),
('adam', 'adam@example.com'),
('ons', 'ons@example.com'),
('jamel', 'jamel@example.com');
>>>>>>> 831940ce815bed44f390c5aae8a6d62fe00914e7
