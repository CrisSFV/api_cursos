#!/usr/bin/env python3
"""
Script para ver TABLAS EN RDS desde local via EC2 (SSH tunnel)
Uso: python3 view_rds_tables.py
"""

import subprocess
import mysql.connector
import sys
import time
import os
import signal

# Configuración
EC2_ID = "i-04c1387964094f50e"
EC2_REGION = "us-east-1"
RDS_HOST = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
RDS_PORT = 3306
RDS_USER = "admin"
RDS_PASSWORD = "Prueba82!"
RDS_DATABASE = "app_db"

tunnel_process = None

def crear_ssh_tunnel():
    """Crear SSH tunnel a EC2 via SSM"""
    global tunnel_process
    
    print("🔗 Creando SSH tunnel a EC2...")
    print("   Ejecutando: aws ssm start-session --target {} --document-name AWS-StartSSHSession".format(EC2_ID))
    
    try:
        # Iniciar el tunnel
        tunnel_process = subprocess.Popen(
            [
                "aws", "ssm", "start-session",
                "--target", EC2_ID,
                "--region", EC2_REGION,
                "--document-name", "AWS-StartSSHSession",
                "--parameters", "portNumber=3306"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("   ✅ Tunnel iniciado")
        time.sleep(2)  # Esperar a que se establezca
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def cerrar_ssh_tunnel():
    """Cerrar SSH tunnel"""
    global tunnel_process
    if tunnel_process:
        print("\n🔌 Cerrando tunnel...")
        tunnel_process.terminate()
        time.sleep(1)

def conectar_rds(host="localhost", puerto=3306):
    """Conectar a RDS"""
    try:
        print(f"\n📡 Conectando a RDS:")
        print(f"   Host: {host}:{puerto}")
        print(f"   Usuario: {RDS_USER}")
        print(f"   BD: {RDS_DATABASE}")
        
        cnx = mysql.connector.connect(
            host=host,
            port=puerto,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )
        
        print("   ✅ Conexión exitosa")
        return cnx
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def mostrar_tablas(cnx):
    """Mostrar todas las tablas en RDS"""
    print("\n" + "="*70)
    print("📊 TABLAS EN RDS (AWS)")
    print("="*70)
    
    try:
        cursor = cnx.cursor()
        
        # SHOW TABLES
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️  No hay tablas aún.")
            print("\n💡 Para crear tablas:")
            print("   1. Conecta a EC2: aws ssm start-session --target i-04c1387964094f50e")
            print("   2. Ejecuta: cd /opt/app && python3 deploy_rds.py")
            return
        
        print(f"\n✅ Total: {len(tables)} tabla(s)\n")
        
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
            
            print(f"📋 {table_name}")
            print(f"   📍 Filas: {row_count}")
            print(f"   🔧 Columnas:")
            
            for col_name, col_type, nullable, col_key in columns:
                pk = "🔑" if col_key == "PRI" else "  "
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"      {pk} {col_name}: {col_type} ({null_str})")
            print()
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def mostrar_status(cnx):
    """Mostrar estado de RDS"""
    print("="*70)
    print("ℹ️  STATUS")
    print("="*70)
    
    try:
        cursor = cnx.cursor()
        
        # Versión
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]
        
        # Tamaño
        cursor.execute("""
            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE();
        """)
        size = cursor.fetchone()[0] or 0
        
        print(f"🗄️  Base de datos: {RDS_DATABASE}")
        print(f"💾 Versión: {version}")
        print(f"📏 Tamaño: {size} MB")
        print(f"🔗 Host RDS: {RDS_HOST}")
        print(f"🖥️  EC2: i-04c1387964094f50e (us-east-1)")
        
        cursor.close()
    except Exception as e:
        print(f"❌ Error: {e}")

# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 VER TABLAS EN RDS (AWS)")
    print("="*70)
    
    # Opción 1: Intenta conexión directa (fallará si firewall bloquea)
    print("\n🔄 Opción 1: Conexión DIRECTA a RDS...")
    cnx = conectar_rds(RDS_HOST, RDS_PORT)
    
    if not cnx:
        # Opción 2: Via SSH tunnel
        print("\n🔄 Opción 2: Conexión via SSH TUNNEL...")
        print("   ⚠️  Esto requiere AWS CLI + SessionManagerPlugin")
        print("   (Si no tienes SessionManagerPlugin, instálalo)")
        
        if crear_ssh_tunnel():
            time.sleep(2)
            cnx = conectar_rds("localhost", 3306)
        else:
            print("\n❌ No se pudo crear tunnel SSH")
            print("\n💡 Alternativa: Conectar a EC2 directamente")
            print("   aws ssm start-session --target i-04c1387964094f50e")
            print("   Luego ejecutar: python3 deploy_rds.py")
            sys.exit(1)
    
    if cnx:
        mostrar_tablas(cnx)
        mostrar_status(cnx)
        cnx.close()
        
        print("\n" + "="*70)
        print("✅ COMPLETADO")
        print("="*70 + "\n")
    
    # Cerrar tunnel si existe
    cerrar_ssh_tunnel()
