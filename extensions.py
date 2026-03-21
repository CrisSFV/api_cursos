from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

swagger = Swagger(template={
    "swagger": "2.0",
    "info": {
        "title": "API de Cursos",
        "version": "1.0.0",
        "description": "API REST para gestionar cursos y categorías con operaciones CRUD completas"
    },
    "host": "localhost:5000",
    "basePath": "/api/v1",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Colocar Bearer Token <tu-token>",
        }
    }
})
