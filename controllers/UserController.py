from flask import Blueprint, request, jsonify
from services.authService import AuthService
from flasgger import swag_from

user_bp = Blueprint('auth', __name__)

@user_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'Usuario creado'},
        400: {'description': 'Error en los datos'}
    }
})
def register():
    data = request.get_json() or {}
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'username, email y password son obligatorios'}), 400
    
    try:
        user = AuthService.register(username, email, password)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@user_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'otp_code': {'type': 'string', 'description': 'Código 2FA si está habilitado'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login exitoso o requiere 2FA'},
        401: {'description': 'Credenciales inválidas'}
    }
})
def login():
    data = request.get_json() or {}
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'username y password son obligatorios'}), 400
    
    otp_code = data.get('otp_code')
    result = AuthService.login(username, password, otp_code)
    if not result:
        return jsonify({'message': 'Credenciales inválidas'}), 401
    
    # Si requiere 2FA, devolver indicador
    if result.get('requires_2fa'):
        return jsonify({
            'requires_2fa': True,
            'message': 'Por favor proporcionar código 2FA',
            'user_id': result['user_id']
        }), 200
    
    return jsonify({
        "access_token": result['access_token'],
        "user": result['user'].to_dict()
    }), 200


@user_bp.route('/2fa/incognito-qr', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'account_name': {'type': 'string'},
                    'issuer_name': {'type': 'string'}
                },
                'required': ['account_name']
            }
        }
    ],
    'responses': {
        200: {'description': 'QR de 2FA generado'},
        400: {'description': 'Datos inválidos'}
    }
})
def generate_incognito_2fa_qr():
    data = request.get_json() or {}
    account_name = data.get('account_name')
    issuer_name = data.get('issuer_name', 'API82')

    if not account_name:
        return jsonify({'message': 'account_name es obligatorio'}), 400

    result = AuthService.generate_incognito_2fa_qr(account_name, issuer_name)
    return jsonify(result), 200
@user_bp.route('/2fa/verify', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'secret': {'type': 'string'},
                    'code': {'type': 'string'}
                },
                'required': ['secret', 'code']
            }
        }
    ],
    'responses': {
        200: {'description': 'Resultado validación 2FA'},
        400: {'description': 'Datos inválidos'}
    }
})
def verify_2fa_code():
    data = request.get_json() or {}
    secret = data.get('secret')
    code = data.get('code')

    if not secret or not code:
        return jsonify({'message': 'secret y code son obligatorios'}), 400

    is_valid = AuthService.verify_2fa_code(secret, code)
    return jsonify({'valid': is_valid}), 200


@user_bp.route('/2fa/enable-qr', methods=['POST'])
@swag_from({
    'tags': ['2FA'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'issuer_name': {'type': 'string'}
                },
                'required': ['user_id']
            }
        }
    ],
    'responses': {
        200: {'description': 'QR para habilitar 2FA'},
        400: {'description': 'Usuario no existe'}
    }
})
def generate_user_2fa_qr():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    issuer_name = data.get('issuer_name', 'API82')

    if not user_id:
        return jsonify({'message': 'user_id es obligatorio'}), 400

    result = AuthService.generate_user_2fa_qr(user_id, issuer_name)
    if not result:
        return jsonify({'message': 'Usuario no existe'}), 400

    return jsonify(result), 200


@user_bp.route('/2fa/enable', methods=['POST'])
@swag_from({
    'tags': ['2FA'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'secret': {'type': 'string'},
                    'otp_code': {'type': 'string'}
                },
                'required': ['user_id', 'secret', 'otp_code']
            }
        }
    ],
    'responses': {
        200: {'description': '2FA habilitado'},
        400: {'description': 'Código OTP inválido o usuario no existe'}
    }
})
def enable_user_2fa():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    secret = data.get('secret')
    otp_code = data.get('otp_code')

    if not user_id or not secret or not otp_code:
        return jsonify({'message': 'user_id, secret y otp_code son obligatorios'}), 400

    success = AuthService.enable_user_2fa(user_id, secret, otp_code)
    if not success:
        return jsonify({'message': 'Código OTP inválido o usuario no existe'}), 400

    return jsonify({'message': '2FA habilitado correctamente'}), 200


@user_bp.route('/2fa/disable', methods=['POST'])
@swag_from({
    'tags': ['2FA'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'password': {'type': 'string'}
                },
                'required': ['user_id', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': '2FA deshabilitado'},
        400: {'description': 'Contraseña inválida o usuario no existe'}
    }
})
def disable_user_2fa():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({'message': 'user_id y password son obligatorios'}), 400

    success = AuthService.disable_user_2fa(user_id, password)
    if not success:
        return jsonify({'message': 'Contraseña inválida o usuario no existe'}), 400

    return jsonify({'message': '2FA deshabilitado correctamente'}), 200