#!/usr/bin/env python3
"""
Script para deployar en RDS (ejecutar desde EC2)
Uso: python3 deploy_rds.py
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

# Configuración RDS
RDS_HOST = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
RDS_PORT = 3306
RDS_USER = "admin"
RDS_PASSWORD = "Prueba82!"
RDS_DATABASE = "app_db"

def crear_bd_si_no_existe():
    """Crear BD si no existe"""
    print("\n1️⃣  Verificando/creando BD en RDS...")
    try:
        # Conectar sin especificar BD
        cnx = mysql.connector.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = cnx.cursor()
        
        # Crear BD
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {RDS_DATABASE} CHARACTER SET utf8mb4;")
        cnx.commit()
        
        existing = cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{RDS_DATABASE}';")
        if cursor.fetchone():
            print(f"   ✅ BD '{RDS_DATABASE}' lista")
        
        cursor.close()
        cnx.close()
        return True
    except Error as e:
        print(f"   ❌ Error: {e}")
        return False

def crear_tablas():
    """Crear tablas usando Flask ORM"""
    print("\n2️⃣  Creando tablas en RDS...")
    try:
        # Asegurarse que puedes importar la app
        sys.path.insert(0, '/opt/app')  # Ruta en EC2
        
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from extensions import db
            db.create_all()
            print("   ✅ Tablas creadas")
            return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def mostrar_tablas():
    """Mostrar todas las tablas en RDS"""
    print("\n3️⃣  📊 TABLAS EN RDS:")
    print("   " + "="*70)
    
    try:
        cnx = mysql.connector.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )
        cursor = cnx.cursor()
        
        # SHOW TABLES
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        if not tables:
            print("   ⚠️  No hay tablas aún")
            return
        
        print(f"   Total: {len(tables)} tabla(s)\n")
        
        for (table_name,) in tables:
            # Información de la tabla
            cursor.execute(f"""
                SELECT 
                    COLUMN_NAME, 
                    COLUMN_TYPE, 
                    IS_NULLABLE,
                    COLUMN_KEY
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{RDS_DATABASE}' 
                AND TABLE_NAME = '{table_name}'
            """)
            
            columns = cursor.fetchall()
            
            # Contar filas
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            
            print(f"   📋 Tabla: {table_name}")
            print(f"      Filas: {row_count}")
            print(f"      Columnas:")
            
            for col_name, col_type, nullable, col_key in columns:
                pk = "🔑 PK" if col_key == "PRI" else ""
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"         • {col_name}: {col_type} {null_str} {pk}")
            print()
        
        cursor.close()
        cnx.close()
        
    except Error as e:
        print(f"   ❌ Error: {e}")

def show_status():
    """Mostrar estado de la conexión"""
    print("\n" + "="*70)
    print("✅ STATUS RDS")
    print("="*70)
    
    try:
        cnx = mysql.connector.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )
        cursor = cnx.cursor()
        
        # Versión
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]
        
        # Tamaño BD
        cursor.execute("""
            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE();
        """)
        size = cursor.fetchone()[0] or 0
        
        print(f"🗄️  Base de datos: {RDS_DATABASE}")
        print(f"💾 Versión: {version}")
        print(f"📏 Tamaño: {size} MB")
        print(f"🔗 Host: {RDS_HOST}")
        
        cursor.close()
        cnx.close()
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 DEPLOY RDS - api_ing_82")
    print("="*70)
    print("Instrucciones:")
    print("1. Conectar a EC2: aws ssm start-session --target i-04c1387964094f50e")
    print("2. Ir a app: cd /opt/app")
    print("3. Ejecutar: python3 deploy_rds.py")
    print("="*70)
    
    # 1. Crear BD
    if not crear_bd_si_no_existe():
        sys.exit(1)
    
    # 2. Crear tablas
    if not crear_tablas():
        print("\n   ⚠️  Creando tablas manualmente...")
        # Fallback manual
        try:
            cnx = mysql.connector.connect(
                host=RDS_HOST,
                port=RDS_PORT,
                user=RDS_USER,
                password=RDS_PASSWORD,
                database=RDS_DATABASE
            )
            cursor = cnx.cursor()
            print("   ✅ Conexión manual establecida")
            cursor.close()
            cnx.close()
        except Error as e:
            print(f"   ❌ Error: {e}")
            sys.exit(1)
    
    # 3. Mostrar tablas
    mostrar_tablas()
    
    # 4. Mostrar status
    show_status()
    
    print("\n" + "="*70)
    print("✅ COMPLETADO")
    print("="*70)
    print("\n📡 Endpoints disponibles en EC2:")
    print("   GET /api/v1/db/tables   → Ver tablas")
    print("   GET /api/v1/db/status   → Info de BD")
    print("   GET /api/v1/db/health   → Health check")
    print("\n")
