#!/usr/bin/env python3
"""
Script para consultar RDS MySQL VÍA EC2
Ejecuta comandos en EC2 a través de AWS Systems Manager SessionManager

Uso: python ec2_rds_query.py [comando]

Comandos:
  python ec2_rds_query.py databases       - Ver BDs en RDS
  python ec2_rds_query.py tables          - Ver tablas en app_db
  python ec2_rds_query.py structure       - Ver estructura de tablas
  python ec2_rds_query.py all             - Ver todo
"""

import subprocess
import sys

EC2_INSTANCE = "i-04c1387964094f50e"
REGION = "us-east-1"

# Credenciales RDS
RDS_HOST = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASS = "Prueba82!"
RDS_DB = "app_db"

def run_ec2_command(cmd):
    """Ejecuta comando en EC2 vía AWS Systems Manager"""
    try:
        full_cmd = [
            "aws", "ssm", "start-session",
            "--target", EC2_INSTANCE,
            "--region", REGION,
            "--document-name", "AWS-StartInteractiveCommand",
            "--parameters", f"command={cmd}"
        ]
        
        # Versión simplificada - ejecutar el comando directamente en EC2
        ec2_cmd = f'aws ssm start-session --target {EC2_INSTANCE} --region {REGION}'
        
        # Crear script temporario en EC2
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(cmd)
            f.flush()
            
            # Ejecutar vía SSM
            result = subprocess.run(
                f'aws ssm start-session --target {EC2_INSTANCE} --region {REGION} --command "\\'{cmd}\\'"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def print_databases():
    """Ver bases de datos"""
    print("\n" + "="*70)
    print("📊 BASES DE DATOS EN RDS (via EC2)")
    print("="*70)
    
    cmd = f'python3 -c "import mysql.connector; c=mysql.connector.connect(host=\\"{RDS_HOST}\\",user=\\"{RDS_USER}\\",password=\\"{RDS_PASS}\\"); cur=c.cursor(); cur.execute(\\"SHOW DATABASES;\\"); [print(f\\"  ✓ {{t[0]}}\\") for t in cur.fetchall()]; c.close()"'
    
    print("\n📍 OPCIÓN 1: Copiar este comando en EC2\n")
    print(cmd)
    
    print("\n" + "="*70)
    print("📍 OPCIÓN 2: O ejecutar desde EC2 directamente:\n")
    print(f'aws ssm start-session --target {EC2_INSTANCE} --region {REGION}')
    print("# Una vez dentro, ejecuta:")
    print(cmd.replace('\\"', '"').replace('\\\\"', '\\"'))
    print("="*70 + "\n")

def print_tables():
    """Ver tablas"""
    print("\n" + "="*70)
    print("📋 TABLAS EN RDS (via EC2)")
    print("="*70)
    
    cmd = f'python3 -c "import mysql.connector; c=mysql.connector.connect(host=\\"{RDS_HOST}\\",user=\\"{RDS_USER}\\",password=\\"{RDS_PASS}\\",database=\\"{RDS_DB}\\"); cur=c.cursor(); cur.execute(\\"SHOW TABLES;\\"); [print(f\\"  ✓ {{t[0]}}\\") for t in cur.fetchall()]; c.close()"'
    
    print("\n📍 Ejecutar en EC2:\n")
    print(cmd.replace('\\"', '"').replace('\\\\"', '\\"'))
    print("\n" + "="*70 + "\n")

def print_structure():
    """Ver estructura"""
    print("\n" + "="*70)
    print("📐 ESTRUCTURA DE TABLAS (via EC2)")
    print("="*70)
    
    tables = ['categories', 'courses']
    
    for table in tables:
        cmd = f'python3 -c "import mysql.connector; c=mysql.connector.connect(host=\\"{RDS_HOST}\\",user=\\"{RDS_USER}\\",password=\\"{RDS_PASS}\\",database=\\"{RDS_DB}\\"); cur=c.cursor(); cur.execute(\\"DESCRIBE {table};\\"); print(f\\"Tabla: {table}\\"); [print(f\\"  {{str(t[0]):20}} {{str(t[1]):30}}\\") for t in cur.fetchall()]; c.close()"'
        
        print(f"\n✏️  Tabla: {table}\n")
        print(cmd.replace('\\"', '"').replace('\\\\"', '\\"'))
    
    print("\n" + "="*70 + "\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n🔗 CONEXIÓN RÁPIDA A EC2:")
        print(f"aws ssm start-session --target {EC2_INSTANCE} --region {REGION}\n")
        return
    
    command = sys.argv[1].lower()
    
    if command == "databases":
        print_databases()
    elif command == "tables":
        print_tables()
    elif command == "structure":
        print_structure()
    elif command == "all":
        print_databases()
        print_tables()
        print_structure()
    else:
        print(f"❌ Comando desconocido: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
