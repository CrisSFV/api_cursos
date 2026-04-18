from flask import Blueprint, request, jsonify
from services.studentService import StudentService
from flasgger import swag_from

student_bp = Blueprint('students', __name__)


@student_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Alumnos'],
    'summary': 'Crear un nuevo alumno',
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
                        'description': 'Nombre del alumno',
                        'example': 'Juan'
                    },
                    'apellido_paterno': {
                        'type': 'string',
                        'description': 'Apellido paterno',
                        'example': 'García'
                    },
                    'apellido_materno': {
                        'type': 'string',
                        'description': 'Apellido materno',
                        'example': 'López'
                    },
                    'matricula': {
                        'type': 'string',
                        'description': 'Número de matrícula (único)',
                        'example': 'A001234567'
                    },
                    'correo': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Correo electrónico',
                        'example': 'juan.garcia@escuela.edu'
                    }
                },
                'required': ['nombre', 'apellido_paterno', 'apellido_materno', 'matricula', 'correo']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Alumno creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'apellido_paterno': {'type': 'string'},
                    'apellido_materno': {'type': 'string'},
                    'matricula': {'type': 'string'},
                    'correo': {'type': 'string'},
                    'fecha_alta': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Error en los datos enviados'
        }
    }
})
def create_student():
    """Crear un nuevo alumno"""
    data = request.get_json() or {}
    
    try:
        nombre = data.get('nombre')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        matricula = data.get('matricula')
        correo = data.get('correo')
        
        if not all([nombre, apellido_paterno, apellido_materno, matricula, correo]):
            return jsonify({
                'error': 'Los campos nombre, apellido_paterno, apellido_materno, matricula y correo son obligatorios'
            }), 400
        
        student = StudentService.create_student(nombre, apellido_paterno, apellido_materno, matricula, correo)
        return jsonify(student.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear el alumno'}), 500


@student_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Alumnos'],
    'summary': 'Obtener alumnos con filtros opcionales',
    'parameters': [
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
            'description': 'Lista de alumnos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'apellido_paterno': {'type': 'string'},
                        'apellido_materno': {'type': 'string'},
                        'matricula': {'type': 'string'},
                        'correo': {'type': 'string'},
                        'fecha_alta': {'type': 'string'}
                    }
                }
            }
        },
        400: {
            'description': 'Error en los parámetros'
        }
    }
})
def get_students():
    """Obtener todos los alumnos con filtros opcionales de fecha"""
    try:
        fecha_inicio = request.args.get('fecha_inicio', default=None)
        fecha_fin = request.args.get('fecha_fin', default=None)
        
        if fecha_inicio or fecha_fin:
            students = StudentService.filter_students_by_date(fecha_inicio, fecha_fin)
        else:
            students = StudentService.get_all_students()
        
        return jsonify([student.to_dict() for student in students]), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al obtener los alumnos'}), 500


@student_bp.route('/<int:student_id>', methods=['GET'])
@swag_from({
    'tags': ['Alumnos'],
    'summary': 'Obtener un alumno por ID',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del alumno'
        }
    ],
    'responses': {
        200: {
            'description': 'Alumno encontrado'
        },
        404: {
            'description': 'Alumno no encontrado'
        }
    }
})
def get_student(student_id):
    """Obtener un alumno por ID"""
    try:
        student = StudentService.get_student(student_id)
        return jsonify(student.to_dict()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener el alumno'}), 500


@student_bp.route('/<int:student_id>', methods=['PUT'])
@swag_from({
    'tags': ['Alumnos'],
    'summary': 'Actualizar un alumno',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del alumno'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'apellido_paterno': {'type': 'string'},
                    'apellido_materno': {'type': 'string'},
                    'correo': {'type': 'string', 'format': 'email'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Alumno actualizado'
        },
        404: {
            'description': 'Alumno no encontrado'
        }
    }
})
def update_student(student_id):
    """Actualizar un alumno"""
    data = request.get_json() or {}
    
    try:
        nombre = data.get('nombre')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        correo = data.get('correo')
        
        student = StudentService.update_student(student_id, nombre, apellido_paterno, apellido_materno, correo)
        return jsonify(student.to_dict()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al actualizar el alumno'}), 500


@student_bp.route('/<int:student_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Alumnos'],
    'summary': 'Eliminar un alumno',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del alumno'
        }
    ],
    'responses': {
        200: {
            'description': 'Alumno eliminado exitosamente'
        },
        404: {
            'description': 'Alumno no encontrado'
        }
    }
})
def delete_student(student_id):
    """Eliminar un alumno"""
    try:
        StudentService.delete_student(student_id)
        return jsonify({'message': 'Alumno eliminado exitosamente'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el alumno'}), 500
