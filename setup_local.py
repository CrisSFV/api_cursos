#!/usr/bin/env python3
"""
Setup rápido de la app con SQLite (desarrollo local)
Uso: python setup_local.py
"""

import os
import sys

def setup_local():
    print("\n" + "="*70)
    print("🚀 SETUP LOCAL - api_ing_82")
    print("="*70)
    
    # 1. Crear app
    print("\n1️⃣  Inicializando aplicación...")
    try:
        from app import create_app
        app = create_app()
        print("   ✅ App creada")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # 2. Crear tablas
    print("\n2️⃣  Creando tablas en SQLite...")
    try:
        with app.app_context():
            from extensions import db
            db.create_all()
            print("   ✅ Tablas creadas")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # 3. Verificar tablas
    print("\n3️⃣  Verificando tablas...")
    try:
        with app.app_context():
            from sqlalchemy import inspect as sa_inspect
            inspector = sa_inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"   ✅ Total tablas: {len(tables)}")
                for i, table in enumerate(tables, 1):
                    cols = len(inspector.get_columns(table))
                    print(f"      {i}. {table} ({cols} columnas)")
            else:
                print("   ⚠️  No hay tablas (modelos no definidos aún)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # 4. Mostrar info de BD
    print("\n4️⃣  Información de BD:")
    try:
        db_path = os.path.abspath("api_ing_82.db")
        if os.path.exists(db_path):
            size = os.path.getsize(db_path) / 1024  # KB
            print(f"   📁 Archivo: {db_path}")
            print(f"   💾 Tamaño: {size:.2f} KB")
        print("   🗄️  Motor: SQLite")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 5. Instrucciones para ejecutar
    print("\n" + "="*70)
    print("✅ SETUP COMPLETADO")
    print("="*70)
    print("\n🚀 Para ejecutar la app:")
    print("\n   python app.py")
    print("\n📡 Endpoints disponibles:")
    print("   GET  http://localhost:5000/                    → Home")
    print("   GET  http://localhost:5000/api/v1/db/health    → Health check")
    print("   GET  http://localhost:5000/api/v1/db/tables    → SHOW TABLES")
    print("   GET  http://localhost:5000/api/v1/db/status    → Info BD")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    setup_local()
