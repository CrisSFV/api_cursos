from flask import Flask
from controllers.HomeController import blueprint_home
from controllers.CourseController import course_bp
from controllers.CategoryController import category_bp
from controllers.DatabaseController import db_bp
from controllers.UserController import user_bp
from extensions import db, migrate, swagger, jwt
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    app.register_blueprint(course_bp, url_prefix='/api/v1/cursos')
    app.register_blueprint(category_bp, url_prefix='/api/v1/categorias')
    app.register_blueprint(user_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(db_bp)  # Esto es para la base de datos
    app.register_blueprint(blueprint_home, url_prefix='/api/v1')

    @app.route('/')
    def home():
        return {'message': 'API de Cursos - Bienvenido'}

    return app

if __name__ == '__main__':
    app = create_app()
    
    # ⚠️ No intentar crear tablas aquí (no puedes conectar desde local)
    # Usar: python shell o script en EC2 para crear_all()
    
    print("\n" + "="*60)
    print("🚀 API inicializando...")
    print("="*60)
    print(f"📍 Base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')[:50]}...")
    print("✅ Para crear tablas en RDS:")
    print("   1. Opción 1: Ejecutar desde EC2")
    print("   2. Opción 2: python -c \"from app import create_app; app=create_app(); app.app_context().push(); from extensions import db; db.create_all()\"")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)