-- Créer la base de données mydb si elle n'existe pas
-- CREATE DATABASE mydb;

-- Accorder tous les privilèges à l'utilisateur quentin
GRANT ALL PRIVILEGES ON DATABASE mydb TO quentin;

-- Appliquer les droits sur les schémas publics (facultatif)
GRANT ALL PRIVILEGES ON SCHEMA public TO quentin;

CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,                  -- Clé primaire automatique
    sensor_id VARCHAR(255) NOT NULL,        -- ID du capteur (texte)
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Timestamp par défaut en UTC
    temperature NUMERIC(5, 2) NOT NULL,     -- Température avec 2 décimales
    humidity INTEGER NOT NULL,              -- Humidité (entier)
    msg TEXT                                -- Message de description (texte)
);
