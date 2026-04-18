#!/usr/bin/env python3
"""
Script simple para crear tablas en RDS
Ejecutar desde: python create_aws_tables.py
"""

import sys

def setup_tables():
    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python no está instalado")
        print("🔧 Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
        import mysql.connector
    
    # Configuración RDS
    RDS_HOST = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
    RDS_USER = "admin"
    RDS_PASSWORD = "Prueba82!"
    RDS_DB = "app_db"
    
    print("\n" + "="*70)
    print("🚀 CREANDO TABLAS EN AWS RDS")
    print("="*70)
    print(f"🔗 Conectando a: {RDS_HOST}")
    
    try:
        # Paso 1: Crear BD
        print("\n1️⃣  Creando BD (si no existe)...")
        cnx = mysql.connector.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = cnx.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {RDS_DB} CHARACTER SET utf8mb4;")
        cnx.commit()
        cursor.close()
        cnx.close()
        print("   ✅ BD 'app_db' lista\n")
        
        # Paso 2: Conectar a la BD
        print("2️⃣  Conectando a BD...")
        cnx = mysql.connector.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB
        )
        cursor = cnx.cursor()
        print("   ✅ Conectado\n")
        
       # Paso 3: Crear tabla 'categories'
        print("3️⃣  Creando tabla 'categories'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(120) NOT NULL,
            description VARCHAR(500),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cnx.commit()
        print("   ✅ Tabla 'categories' creada\n")
        
        # Paso 4: Crear tabla 'courses'
        print("4️⃣  Creando tabla 'courses'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            descripcion TEXT NOT NULL,
            precio FLOAT NOT NULL,
            categoria_id INT NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categories(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cnx.commit()
        print("   ✅ Tabla 'courses' creada\n")
        
        # Paso 5: Verificar tablas creadas
        print("5️⃣  📊 TABLAS EN RDS:")
        print("   " + "="*68)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESC {table_name};")
            columns = cursor.fetchall()
            print(f"\n   📋 {table_name.upper()} ({len(columns)} columnas)")
            for col in columns:
                col_name, col_type, nullable, col_key, col_default, col_extra = col
                pk = "🔑 PK" if col_key == "PRI" else "  "
                print(f"      {pk} {col_name}: {col_type}")
        
        cursor.close()
        cnx.close()
        
        print("\n   " + "="*68)
        print("\n" + "="*70)
        print("✅ ¡ÉXITO! Tablas creadas en AWS RDS")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    setup_tables()
