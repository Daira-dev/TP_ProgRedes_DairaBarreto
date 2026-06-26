-- Crear base de datos
CREATE DATABASE IF NOT EXISTS tp_redes;

USE tp_redes;

-- Tabla de usuarios del sistema
CREATE TABLE IF NOT EXISTS usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(50) NOT NULL UNIQUE,
clave VARCHAR(50) NOT NULL
);

-- Tabla de repositorios obtenidos desde GitHub
CREATE TABLE IF NOT EXISTS repositorios (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(100) NOT NULL,
nombre_repo VARCHAR(200) NOT NULL,
url_repo VARCHAR(300) NOT NULL
);

-- Tabla de followers obtenidos desde GitHub
CREATE TABLE IF NOT EXISTS followers (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(100) NOT NULL,
seguidor VARCHAR(100) NOT NULL,
tipo VARCHAR(50),
url_follower VARCHAR(300)
);

-- Usuarios de prueba
INSERT IGNORE INTO usuarios (usuario, clave)
VALUES
('daira', '1234'),
('profe', '1234');
