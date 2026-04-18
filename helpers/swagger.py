"""
Esquemas y decoradores Swagger para la API
Uso: from helpers.swagger import register_schema, login_schema, etc
"""

# ===========================
# ESQUEMAS DE AUTENTICACIÓN
# ===========================
register_schema = {
    'tags': ['Autenticación'],
    'summary': 'Registrar nuevo usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'juan_doe',
                        'description': 'Nombre de usuario único'
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'example': 'juan@example.com',
                        'description': 'Correo electrónico válido'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'Password123!',
                        'description': 'Contraseña (mín. 8 caracteres)'
                    }
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'twofa_enabled': {'type': 'boolean'}
                }
            }
        },
        400: {'description': 'Error de validación'},
        409: {'description': 'Usuario ya existe'}
    }
}

login_schema = {
    'tags': ['Autenticación'],
    'summary': 'Login de usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'juan_doe'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'Password123!'
                    },
                    'otp_code': {
                        'type': 'string',
                        'example': '123456',
                        'description': 'Código 2FA (opcional)'
                    }
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'},
                    'user': {'type': 'object'}
                }
            }
        },
        401: {'description': 'Credenciales inválidas'},
        403: {'description': 'Requiere 2FA'}
    }
}

# ===========================
# ESQUEMAS DE CURSOS
# ===========================
create_course_schema = {
    'tags': ['Cursos'],
    'summary': 'Crear nuevo curso',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'example': 'Bearer eyJhbGc...',
            'description': 'JWT Token'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {
                        'type': 'string',
                        'example': 'Python Avanzado'
                    },
                    'descripcion': {
                        'type': 'string',
                        'example': 'Aprende Python a nivel avanzado'
                    },
                    'precio': {
                        'type': 'number',
                        'format': 'float',
                        'example': 99.99
                    },
                    'categoria_id': {
                        'type': 'integer',
                        'example': 1
                    }
                },
                'required': ['nombre', 'descripcion', 'precio', 'categoria_id']
            }
        }
    ],
    'responses': {
        201: {'description': 'Curso creado'},
        400: {'description': 'Error de validación'},
        401: {'description': 'No autorizado'}
    }
}

get_courses_schema = {
    'tags': ['Cursos'],
    'summary': 'Obtener cursos (con filtros opcionales)',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'example': 1
        },
        {
            'name': 'fecha_inicio',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'example': '2026-01-01'
        },
        {
            'name': 'fecha_fin',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'example': '2026-12-31'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de cursos',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        }
    }
}

# ===========================
# ESQUEMAS DE CATEGORÍAS
# ===========================
create_category_schema = {
    'tags': ['Categorías'],
    'summary': 'Crear nueva categoría',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'example': 'Bearer eyJhbGc...'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Programación'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Cursos de programación'
                    }
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        201: {'description': 'Categoría creada'},
        400: {'description': 'Error de validación'},
        401: {'description': 'No autorizado'}
    }
}
