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
