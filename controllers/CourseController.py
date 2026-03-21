from flask import Blueprint, request, jsonify
from services.courseService import CourseService
from flasgger import swag_from

course_bp = Blueprint('courses', __name__)


@course_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Crear un nuevo curso',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {
                        'type': 'string',
                        'description': 'Nombre del curso',
                        'example': 'Python Básico'
                    },
                    'descripcion': {
                        'type': 'string',
                        'description': 'Descripción del curso',
                        'example': 'Aprende los fundamentos de Python'
                    },
                    'precio': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Precio del curso',
                        'example': 49.99
                    },
                    'categoria_id': {
                        'type': 'integer',
                        'description': 'ID de la categoría',
                        'example': 1
                    }
                },
                'required': ['nombre', 'descripcion', 'precio', 'categoria_id']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Curso creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'descripcion': {'type': 'string'},
                    'precio': {'type': 'number'},
                    'categoria': {'type': 'object'},
                    'fecha_creacion': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Error en los datos enviados'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def create_course():
    """Crear un nuevo curso"""
    data = request.get_json() or {}
    
    try:
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        categoria_id = data.get('categoria_id')
        
        # Validaciones básicas
        if not all([nombre, descripcion, precio is not None, categoria_id]):
            return jsonify({
                'error': 'Los campos nombre, descripcion, precio y categoria_id son obligatorios'
            }), 400
        
        course = CourseService.create_course(nombre, descripcion, precio, categoria_id)
        return jsonify(course.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear el curso'}), 500


@course_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Obtener cursos con filtros opcionales',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'ID de la categoría para filtrar'
        },
        {
            'name': 'fecha_inicio',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'description': 'Fecha de inicio (YYYY-MM-DD)'
        },
        {
            'name': 'fecha_fin',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'description': 'Fecha de fin (YYYY-MM-DD)'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de cursos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'precio': {'type': 'number'},
                        'categoria': {'type': 'object'},
                        'fecha_creacion': {'type': 'string'}
                    }
                }
            }
        },
        400: {
            'description': 'Error en los parámetros'
        }
    }
})
def get_courses():
    """Obtener todos los cursos con filtros opcionales"""
    try:
        categoria = request.args.get('categoria', type=int)
        fecha_inicio = request.args.get('fecha_inicio', default=None)
        fecha_fin = request.args.get('fecha_fin', default=None)
        
        # Si hay filtros, usar filtro_courses, sino obtener todos
        if categoria or fecha_inicio or fecha_fin:
            courses = CourseService.filter_courses(categoria, fecha_inicio, fecha_fin)
        else:
            courses = CourseService.get_all_courses()
        
        return jsonify([course.to_dict() for course in courses]), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al obtener los cursos'}), 500


@course_bp.route('/<int:course_id>', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Obtener un curso por ID',
    'parameters': [
        {
            'name': 'course_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        }
    ],
    'responses': {
        200: {
            'description': 'Curso encontrado'
        },
        404: {
            'description': 'Curso no encontrado'
        }
    }
})
def get_course(course_id):
    """Obtener un curso por ID"""
    try:
        course = CourseService.get_course(course_id)
        return jsonify(course.to_dict()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener el curso'}), 500


@course_bp.route('/<int:course_id>', methods=['PUT'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Actualizar un curso',
    'parameters': [
        {
            'name': 'course_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'descripcion': {'type': 'string'},
                    'precio': {'type': 'number'},
                    'categoria_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Curso actualizado'
        },
        404: {
            'description': 'Curso no encontrado'
        }
    }
})
def update_course(course_id):
    """Actualizar un curso"""
    data = request.get_json() or {}
    
    try:
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        categoria_id = data.get('categoria_id')
        
        course = CourseService.update_course(course_id, nombre, descripcion, precio, categoria_id)
        return jsonify(course.to_dict()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al actualizar el curso'}), 500


@course_bp.route('/<int:course_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Eliminar un curso',
    'parameters': [
        {
            'name': 'course_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        }
    ],
    'responses': {
        200: {
            'description': 'Curso eliminado exitosamente'
        },
        404: {
            'description': 'Curso no encontrado'
        }
    }
})
def delete_course(course_id):
    """Eliminar un curso"""
    try:
        CourseService.delete_course(course_id)
        return jsonify({'message': 'Curso eliminado exitosamente'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el curso'}), 500
