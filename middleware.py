from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from repositories.userRepository import UserRepository


def token_required(f):
    """
    Decorador para proteger endpoints que requieren autenticación JWT.
    Valida que el token sea válido y que el usuario exista.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verifica el JWT en el header Authorization
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Verifica que el usuario exista
            user = UserRepository.find_by_id(int(user_id))
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            # Pasa el usuario al endpoint
            return f(user, *args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': 'No autorizado'}), 401
    
    return decorated_function


def admin_required(f):
    """
    Decorador para proteger endpoints que requieren role de admin.
    (Implementar cuando se agregue role a User model)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            user = UserRepository.find_by_id(int(user_id))
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            # TODO: Validar que sea admin
            # if not user.is_admin:
            #     return jsonify({'error': 'Acceso denegado. Admin requerido'}), 403
            
            return f(user, *args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': 'No autorizado'}), 401
    
    return decorated_function
