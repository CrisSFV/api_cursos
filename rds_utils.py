"""
Utilidades para conectar y consultar RDS MySQL
Usa Python en EC2 vía AWS Systems Manager
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import subprocess
import json

load_dotenv()

class RDSConnection:
    """Maneja conexiones a RDS MySQL vía EC2"""
    
    def __init__(self, use_ec2=True):
        """Inicializa con credenciales de .env"""
        self.host = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
        self.user = "admin"
        self.password = "Prueba82!"
        self.database = "app_db"
        self.port = 3306
        self.connection = None
        self.use_ec2 = use_ec2
        self.ec2_instance = "i-04c1387964094f50e"
        self.region = "us-east-1"
    
    def connect(self, database=None):
        """Conecta a RDS"""
        try:
            db = database or self.database
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db,
                port=self.port
            )
            print(f"✅ Conectado a RDS: {self.host} (BD: {db})")
            return self.connection
        except Error as e:
            print(f"❌ Error conectando a RDS: {e}")
            return None
    
    def close(self):
        """Cierra la conexión"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión cerrada")
    
    def execute_query(self, query):
        """Ejecuta una query y devuelve resultados"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error ejecutando query: {e}")
            return None
    
    def get_databases(self):
        """Obtiene todas las bases de datos"""
        self.connect()
        databases = self.execute_query("SHOW DATABASES;")
        self.close()
        return databases
    
    def get_tables(self, database=None):
        """Obtiene todas las tablas de una BD"""
        db = database or self.database
        self.connect(db)
        tables = self.execute_query(f"SHOW TABLES;")
        self.close()
        return tables
    
    def get_table_structure(self, table_name):
        """Obtiene la estructura de una tabla"""
        self.connect(self.database)
        structure = self.execute_query(f"DESCRIBE {table_name};")
        self.close()
        return structure
    
    def get_table_count(self, table_name):
        """Obtiene el conteo de registros de una tabla"""
        self.connect(self.database)
        result = self.execute_query(f"SELECT COUNT(*) FROM {table_name};")
        self.close()
        return result[0][0] if result else 0


def print_databases():
    """Imprime todas las bases de datos"""
    print("\n" + "="*70)
    print("📊 BASES DE DATOS EN RDS")
    print("="*70)
    rds = RDSConnection()
    databases = rds.get_databases()
    if databases:
        for db in databases:
            print(f"  ✓ {db[0]}")
    print("="*70 + "\n")


def print_tables(database="app_db"):
    """Imprime tabla de una BD"""
    print("\n" + "="*70)
    print(f"📋 TABLAS EN {database.upper()}")
    print("="*70)
    rds = RDSConnection()
    tables = rds.get_tables(database)
    if tables:
        for table in tables:
            rds.connect(database)
            count = rds.get_table_count(table[0])
            print(f"  ✓ {table[0]:20} ({count} registros)")
            rds.close()
    print("="*70 + "\n")


def print_table_structure(table_name, database="app_db"):
    """Imprime la estructura de una tabla"""
    print("\n" + "="*70)
    print(f"📐 ESTRUCTURA: {table_name.upper()} ({database})")
    print("="*70)
    rds = RDSConnection()
    structure = rds.get_table_structure(table_name)
    if structure:
        print(f"\n{'Field':20} {'Type':30} {'Null':10} {'Key':10}")
        print("-" * 70)
        for col in structure:
            field = str(col[0]) if isinstance(col[0], bytes) else col[0]
            col_type = str(col[1]) if isinstance(col[1], bytes) else col[1]
            null = str(col[2]) if isinstance(col[2], bytes) else col[2]
            key = str(col[3]) if len(col) > 3 else ""
            print(f"{field:20} {col_type:30} {null:10} {key:10}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Ejemplos de uso
    print("\n🔌 UTILIDADES RDS MYSQL\n")
    
    # Ver todas las bases de datos
    print_databases()
    
    # Ver tablas de app_db
    print_tables("app_db")
    
    # Ver estructura de categories
    print_table_structure("categories", "app_db")
    print_table_structure("courses", "app_db")
