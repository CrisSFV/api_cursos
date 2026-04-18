#!/usr/bin/env python3
"""
Script para consultar RDS MySQL desde cmder
Uso: python view_rds.py [comando] [args]

Comandos:
  python view_rds.py databases              - Ver todas las BDs
  python view_rds.py tables                 - Ver tablas de app_db
  python view_rds.py tables <database>      - Ver tablas de una BD específica
  python view_rds.py structure <tabla>      - Ver estructura de una tabla
  python view_rds.py count <tabla>          - Contar registros de una tabla
  python view_rds.py all                    - Ver todo (BDs, tablas y estructuras)
"""

import sys
from rds_utils import (
    RDSConnection,
    print_databases,
    print_tables,
    print_table_structure
)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "databases":
        print_databases()
    
    elif command == "tables":
        database = sys.argv[2] if len(sys.argv) > 2 else "app_db"
        print_tables(database)
    
    elif command == "structure":
        if len(sys.argv) < 3:
            print("❌ Uso: python view_rds.py structure <tabla>")
            return
        table = sys.argv[2]
        database = sys.argv[3] if len(sys.argv) > 3 else "app_db"
        print_table_structure(table, database)
    
    elif command == "count":
        if len(sys.argv) < 3:
            print("❌ Uso: python view_rds.py count <tabla>")
            return
        table = sys.argv[2]
        rds = RDSConnection()
        rds.connect("app_db")
        count = rds.get_table_count(table)
        rds.close()
        print(f"\n📊 {table}: {count} registros\n")
    
    elif command == "all":
        print_databases()
        print_tables("app_db")
        print_table_structure("categories")
        print_table_structure("courses")
    
    else:
        print(f"❌ Comando desconocido: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
