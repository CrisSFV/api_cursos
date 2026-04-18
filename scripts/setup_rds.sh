#!/bin/bash
# Script para crear tablas en AWS RDS
# Uso: bash setup_rds.sh

set -e

echo "======================================"
echo "🗄️ Setup AWS RDS"
echo "======================================"

# Variables
DB_HOST="${1:?Proporciona el host de RDS}"
DB_USER="${2:?Proporciona el usuario de BD}"
DB_PASS="${3:?Proporciona la contraseña de BD}"
DB_NAME="${4:-app_db}"
DB_PORT="${5:-3306}"

echo "📍 Conectando a RDS: $DB_HOST:$DB_PORT"
echo "🗄️ Base de datos: $DB_NAME"

# 1. Crear base de datos si no existe
echo "📦 Creando base de datos..."
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" -e "
    CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` 
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    USE \`$DB_NAME\`;
    
    -- Crear tabla de usuarios
    CREATE TABLE IF NOT EXISTS \`users\` (
        \`id\` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        \`username\` VARCHAR(80) UNIQUE NOT NULL,
        \`email\` VARCHAR(80) UNIQUE NOT NULL,
        \`password\` VARCHAR(128) NOT NULL,
        \`twofa_secret\` VARCHAR(32) NULL,
        \`twofa_enabled\` BOOLEAN DEFAULT FALSE,
        \`created_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        \`updated_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    
    -- Crear tabla de categorías
    CREATE TABLE IF NOT EXISTS \`categories\` (
        \`id\` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        \`name\` VARCHAR(120) UNIQUE NOT NULL,
        \`description\` VARCHAR(500),
        \`created_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Crear tabla de cursos
    CREATE TABLE IF NOT EXISTS \`courses\` (
        \`id\` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        \`nombre\` VARCHAR(200) NOT NULL,
        \`descripcion\` LONGTEXT NOT NULL,
        \`precio\` FLOAT NOT NULL,
        \`categoria_id\` INT NOT NULL,
        \`fecha_creacion\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        \`updated_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (\`categoria_id\`) REFERENCES \`categories\`(\`id\`)
    );
    
    -- Crear tabla de estudiantes
    CREATE TABLE IF NOT EXISTS \`students\` (
        \`id\` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        \`nombre\` VARCHAR(120) NOT NULL,
        \`correo\` VARCHAR(120) UNIQUE NOT NULL,
        \`matricula\` VARCHAR(50) UNIQUE NOT NULL,
        \`carrera\` VARCHAR(120),
        \`created_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"

echo "✅ Tablas creadas exitosamente"

# 2. Crear índices
echo "📑 Creando índices..."
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "
    CREATE INDEX IF NOT EXISTS \`idx_categoria_id\` ON \`courses\`(\`categoria_id\`);
    CREATE INDEX IF NOT EXISTS \`idx_fecha_creacion\` ON \`courses\`(\`fecha_creacion\`);
    CREATE INDEX IF NOT EXISTS \`idx_email\` ON \`users\`(\`email\`);
    CREATE INDEX IF NOT EXISTS \`idx_username\` ON \`users\`(\`username\`);
"

echo "✅ Índices creados exitosamente"

echo "======================================"
echo "✅ Setup RDS completado"
echo "======================================"
echo "💾 Base de datos lista: $DB_NAME"
