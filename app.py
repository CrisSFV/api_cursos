from flask import Flask
from controllers.HomeController import blueprint_home
from controllers.CourseController import course_bp
from controllers.CategoryController import category_bp
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
    app.register_blueprint(blueprint_home, url_prefix='/api/v1')

    @app.route('/')
    def home():
        return {'message': 'API de Cursos - Bienvenido'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)