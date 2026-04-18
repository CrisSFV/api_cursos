from flask import Blueprint, request, jsonify
from repositories.studentRepository import StudentRepository
from flask_jwt_extended import create_access_token, create_refresh_token
from flasgger import swag_from
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Login de alumno',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'matricula': {
                        'type': 'string',
                        'description': 'Matrícula del alumno',
                        'example': 'A001234567'
                    },
                    'correo': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Correo del alumno',
                        'example': 'juan.garcia@escuela.edu'
                    }
                },
                'required': ['matricula', 'correo']
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
                    'refresh_token': {'type': 'string'},
                    'student': {'type': 'object'}
                }
            }
        },
        401: {
            'description': 'Credenciales inválidas'
        },
        400: {
            'description': 'Parámetros faltantes'
        }
    }
})
def login():
    """Login de alumno con matrícula y correo"""
    data = request.get_json() or {}
    
    try:
        matricula = data.get('matricula')
        correo = data.get('correo')
        
        if not matricula or not correo:
            return jsonify({'error': 'Matrícula y correo son obligatorios'}), 400
        
        # Buscar alumno por matrícula y correo
        student = StudentRepository.get_by_matricula(matricula)
        
        if not student:
            return jsonify({'error': 'Credenciales inválidas (matrícula no encontrada)'}), 401
        
        # Verificar que el correo coincida
        if student.correo != correo:
            return jsonify({'error': 'Credenciales inválidas (correo no coincide)'}), 401
        
        # Crear tokens JWT
        access_token = create_access_token(
            identity=student.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(
            identity=student.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'student': student.to_dict(),
            'message': 'Login exitoso'
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Error al procesar el login'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Refrescar token de acceso',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token (refresh_token)',
            'example': 'Bearer <tu-refresh-token>'
        }
    ],
    'responses': {
        200: {
            'description': 'Token refrescado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Token inválido o expirado'
        }
    }
})
def refresh():
    """Refrescar token de acceso usando refresh token"""
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        
        # Crear nuevo access_token
        new_access_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            'access_token': new_access_token,
            'message': 'Token refrescado exitosamente'
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Token inválido'}), 401


@auth_bp.route('/verify', methods=['GET'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Verificar si el token es válido',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token',
            'example': 'Bearer <tu-access-token>'
        }
    ],
    'responses': {
        200: {
            'description': 'Token válido',
            'schema': {
                'type': 'object',
                'properties': {
                    'student_id': {'type': 'integer'},
                    'message': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Token inválido o expirado'
        }
    }
})
def verify():
    """Verificar si el token es válido"""
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        
        student = StudentRepository.get_by_id(current_user_id)
        if not student:
            return jsonify({'error': 'Alumno no encontrado'}), 404
        
        return jsonify({
            'student_id': current_user_id,
            'student': student.to_dict(),
            'message': 'Token válido'
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Token inválido'}), 401
