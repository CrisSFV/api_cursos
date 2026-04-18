#!/usr/bin/env python3
"""
Script para probar conexión a RDS y ver tablas
Uso: python test_rds_connection.py
"""

import os
import sys
from dotenv import load_dotenv
from app import create_app

# Cargar variables de entorno
load_dotenv()

def test_rds_connection():
    """Prueba la conexión a RDS y muestra las tablas"""
    
    print("\n" + "="*60)
    print("🔍 PRUEBA DE CONEXIÓN A RDS MySQL")
    print("="*60)
    
    # Crear app Flask
    app = create_app()
    
    with app.app_context():
        from flask_sqlalchemy import inspect
        from sqlalchemy import text, inspect as sa_inspect
        
        # Obtener la conexión
        inspector = sa_inspect(app.extensions['sqlalchemy'].engine)
        
        # 1. Información de la conexión
        print("\n✅ CONEXIÓN EXITOSA")
        db_url = os.getenv('DATABASE_URI')
        print(f"📍 Database URL: {db_url.split('@')[1] if '@' in db_url else 'N/A'}")
        
        # 2. Obtener el nombre de la BD
        try:
            result = app.extensions['sqlalchemy'].session.execute(text("SELECT DATABASE();"))
            current_db = result.scalar()
            print(f"📚 Base de datos actual: {current_db}")
        except Exception as e:
            print(f"❌ Error obteniendo BD: {e}")
        
        # 3. SHOW TABLES
        print("\n📋 TABLAS EN LA BASE DE DATOS:")
        print("-" * 60)
        
        tables = inspector.get_table_names()
        
        if tables:
            for i, table in enumerate(tables, 1):
                # Obtener columnas
                columns = inspector.get_columns(table)
                col_info = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
                print(f"\n  {i}. {table}")
                print(f"     Columnas: {col_info}")
                print(f"     Total: {len(columns)} columnas")
        else:
            print("\n  ⚠️  No hay tablas en la base de datos")
            print("  Ejecuta: app.run() para crear las tablas automáticamente")
        
        # 4. Información adicional de la BD
        print("\n📊 INFORMACIÓN DE LA BASE DE DATOS:")
        print("-" * 60)
        
        # Tamaño de la BD
        try:
            result = app.extensions['sqlalchemy'].session.execute(
                text("""
                SELECT 
                    TABLE_SCHEMA,
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Tamaño (MB)'
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                GROUP BY TABLE_SCHEMA;
                """)
            )
            for row in result:
                print(f"✅ Tamaño total: {row[1]} MB")
        except Exception as e:
            print(f"⚠️  No se pudo obtener tamaño: {e}")
        
        # Versión de MySQL
        try:
            result = app.extensions['sqlalchemy'].session.execute(text("SELECT VERSION();"))
            version = result.scalar()
            print(f"✅ Versión MySQL: {version}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)
        print("✅ PRUEBA COMPLETADA")
        print("="*60 + "\n")

if __name__ == '__main__':
    try:
        test_rds_connection()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nVerifica que:")
        print("  1. El archivo .env tiene la URL correcta de RDS")
        print("  2. EC2 puede conectar a RDS (revisá Security Groups)")
        print("  3. MySQL está activo en RDS\n")
        sys.exit(1)
