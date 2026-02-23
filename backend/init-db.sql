-- Script de inicialización para PostgreSQL en Docker
-- Se ejecuta automáticamente al crear el contenedor

-- Crear la base de datos si no existe
SELECT 'CREATE DATABASE nationmind_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nationmind_db')\gexec

-- Conectar a la base de datos
\c nationmind_db;

-- Mensaje de confirmación
SELECT 'Base de datos nationmind_db creada exitosamente' AS status;
