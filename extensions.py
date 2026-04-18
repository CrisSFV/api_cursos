from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

swagger = Swagger(
    config={
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    },
    template={
        "swagger": "2.0",
        "info": {
            "title": "API de Gestión de Cursos",
            "version": "2.0.0",
            "description": "API REST para gestionar cursos y categorías con autenticación JWT",
            "contact": {
                "name": "API Support",
                "email": "support@api-cursos.com"
            }
        },
        "host": "localhost:5000",
        "basePath": "/api/v1",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Token. Ej: Bearer eyJhbGc...",
            }
        },
        "security": [
            {"BearerAuth": []}
        ]
    }
)
