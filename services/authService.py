from repositories.userRepository import UserRepository
from flask_jwt_extended import create_access_token
from datetime import timedelta
import base64
from io import BytesIO

import pyotp
import qrcode

class AuthService:
    @staticmethod
    def register(username, email, password):
        return UserRepository.create(username, email, password)
    
    @staticmethod
    def login(username, password, otp_code=None):
        user = UserRepository.find_by_username(username)
        if not user or not user.check_password(password):
            return None
        
        # Si 2FA está habilitado, requerir código OTP
        if user.twofa_enabled:
            if not otp_code:
                return {"requires_2fa": True, "user_id": user.id}
            if not user.verify_totp(otp_code):
                return None
        
        claims = {
            'username': user.username,
        }

        token = create_access_token(
            identity=str(user.id),
            additional_claims=claims,
            expires_delta=timedelta(hours=2)
        )
        return {"access_token": token, 'user': user}

    @staticmethod
    def generate_incognito_2fa_qr(account_name, issuer_name="API82"):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp_auth_url = totp.provisioning_uri(name=account_name, issuer_name=issuer_name)

        qr_image = qrcode.make(otp_auth_url)
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "secret": secret,
            "otp_auth_url": otp_auth_url,
            "qr_image_base64": qr_base64,
            "qr_image_data_url": f"data:image/png;base64,{qr_base64}"
        }

    @staticmethod
    def verify_2fa_code(secret, code):
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

    @staticmethod
    def generate_user_2fa_qr(user_id, issuer_name="API82"):
        """Genera QR para habilitar 2FA en un usuario existente"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            return None
        
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        account_name = f"{user.username} ({user.email})"
        otp_auth_url = totp.provisioning_uri(name=account_name, issuer_name=issuer_name)

        qr_image = qrcode.make(otp_auth_url)
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "secret": secret,
            "otp_auth_url": otp_auth_url,
            "qr_image_base64": qr_base64,
            "qr_image_data_url": f"data:image/png;base64,{qr_base64}"
        }

    @staticmethod
    def enable_user_2fa(user_id, secret, otp_code):
        """Habilita 2FA para un usuario después de validar el código OTP"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False
        
        totp = pyotp.TOTP(secret)
        if not totp.verify(otp_code, valid_window=1):
            return False
        
        user.enable_twofa(secret)
        UserRepository.save(user)
        return True

    @staticmethod
    def disable_user_2fa(user_id, password):
        """Deshabilita 2FA para un usuario (requiere contraseña)"""
        user = UserRepository.find_by_id(user_id)
        if not user or not user.check_password(password):
            return False
        
        user.disable_twofa()
        UserRepository.save(user)
        return True