"""
Controlador para información de Base de Datos
Endpoints:
  - GET /api/v1/db/status - Info de conexión
  - GET /api/v1/db/tables - Lista de tablas
  - GET /api/v1/db/health - Health check
Compatible con: SQLite + MySQL RDS
"""

from flask import Blueprint, jsonify
from sqlalchemy import text, inspect as sa_inspect
from extensions import db
import os

db_bp = Blueprint('database', __name__, url_prefix='/api/v1/db')

def get_db_type():
    """Detectar tipo de base de datos: sqlite o mysql"""
    db_uri = str(db.engine.url)
    if 'sqlite' in db_uri:
        return 'sqlite'
    elif 'mysql' in db_uri:
        return 'mysql'
    return 'unknown'

def get_db_name():
    """Obtener nombre de la base de datos según el tipo"""
    db_type = get_db_type()
    
    if db_type == 'sqlite':
        # Para SQLite, obtener el nombre del archivo
        db_uri = str(db.engine.url)
        if 'sqlite://///' in db_uri:
            # Ruta absoluta
            return db_uri.split('sqlite:////')[1]
        elif 'sqlite:///' in db_uri:
            # Ruta relativa
            return db_uri.split('sqlite:///')[1]
        return 'memory'
    else:
        # Para MySQL, usar SELECT DATABASE()
        try:
            result = db.session.execute(text("SELECT DATABASE();"))
            return result.scalar()
        except:
            return 'unknown'

def get_db_version():
    """Obtener versión de la base de datos"""
    db_type = get_db_type()
    
    if db_type == 'sqlite':
        try:
            result = db.session.execute(text("SELECT sqlite_version();"))
            return f"SQLite {result.scalar()}"
        except:
            return "SQLite (versión desconocida)"
    else:
        try:
            result = db.session.execute(text("SELECT VERSION();"))
            return result.scalar()
        except:
            return "MySQL (versión desconocida)"

def get_db_size():
    """Obtener tamaño de la base de datos"""
    db_type = get_db_type()
    
    if db_type == 'sqlite':
        try:
            # Para SQLite
            result = db.session.execute(text("PRAGMA page_count;"))
            page_count = result.scalar() or 0
            result = db.session.execute(text("PRAGMA page_size;"))
            page_size = result.scalar() or 4096
            size_bytes = page_count * page_size
            size_mb = size_bytes / (1024 * 1024)
            return round(size_mb, 2)
        except:
            return 0
    else:
        try:
            # Para MySQL
            result = db.session.execute(text("""
                SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE();
            """))
            return result.scalar() or 0
        except:
            return 0

@db_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check de la BD
    Retorna: Estado de la conexión a RDS
    """
    try:
        result = db.session.execute(text("SELECT 1"))
        return jsonify({
            'status': 'healthy',
            'message': '✅ Conexión a RDS activa',
            'code': 200
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'❌ Error de conexión: {str(e)}',
            'code': 500
        }), 500

@db_bp.route('/status', methods=['GET'])
def database_status():
    """
    Información detallada de la base de datos
    Retorna: Nombre BD, versión, tamaño, etc.
    Compatible con SQLite y MySQL
    """
    try:
        db_type = get_db_type()
        current_db = get_db_name()
        version = get_db_version()
        size_mb = get_db_size()
        
        return jsonify({
            'status': 'success',
            'database': current_db,
            'database_type': db_type.upper(),
            'version': version,
            'size_mb': float(size_mb),
            'connection': 'SQLite (Local)' if db_type == 'sqlite' else 'MySQL RDS (Producción)'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@db_bp.route('/tables', methods=['GET'])
def show_tables():
    """
    SHOW TABLES - Lista todas las tablas de la BD
    Retorna: Lista de tablas con sus columnas y tipos
    Compatible con SQLite y MySQL
    """
    try:
        # Usar inspector de SQLAlchemy
        inspector = sa_inspect(db.engine)
        
        # Nombre de la BD
        current_db = get_db_name()
        
        # Get all tables
        tables_list = inspector.get_table_names()
        
        tables_info = []
        
        for table_name in tables_list:
            # Obtener columnas
            columns = inspector.get_columns(table_name)
            
            # Obtener primary key
            pk = inspector.get_pk_constraint(table_name)
            
            # Format columns info
            columns_info = []
            for col in columns:
                columns_info.append({
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'primary_key': col['name'] in (pk.get('constrained_columns', []) or [])
                })
            
            tables_info.append({
                'name': table_name,
                'columns_count': len(columns),
                'columns': columns_info
            })
        
        return jsonify({
            'status': 'success',
            'database': current_db,
            'database_type': get_db_type().upper(),
            'tables_count': len(tables_list),
            'tables': tables_info
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@db_bp.route('/tables/<table_name>', methods=['GET'])
def table_info(table_name):
    """
    Información detallada de una tabla específica
    Retorna: Estructura de la tabla (columnas, tipos, constraints)
    """
    try:
        inspector = sa_inspect(db.engine)
        
        # Validar que la tabla existe
        tables = inspector.get_table_names()
        if table_name not in tables:
            return jsonify({
                'status': 'error',
                'message': f'Tabla "{table_name}" no existe'
            }), 404
        
        # Get table info
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name)
        fks = inspector.get_foreign_keys(table_name)
        
        # Format response
        columns_info = []
        for col in columns:
            columns_info.append({
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': col.get('default'),
                'primary_key': col['name'] in (pk.get('constrained_columns', []) or [])
            })
        
        fks_info = []
        for fk in fks:
            fks_info.append({
                'name': fk.get('name'),
                'columns': fk.get('constrained_columns'),
                'refers_to': f"{fk.get('referred_table')}.{fk.get('referred_columns')}"
            })
        
        # Count rows
        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
        row_count = result.scalar()
        
        return jsonify({
            'status': 'success',
            'table': table_name,
            'columns_count': len(columns),
            'rows_count': row_count,
            'columns': columns_info,
            'foreign_keys': fks_info if fks_info else []
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
