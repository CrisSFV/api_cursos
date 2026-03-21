from extensions import db
from passlib.hash import bcrypt,pbkdf2_sha256
import pyotp

class User(db.Model):
    __tablename__ ='users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    twofa_secret = db.Column(db.String(32), nullable=True, default=None)
    twofa_enabled = db.Column(db.Boolean, nullable=False, default=False)
    
    def set_password(self, password: str):
        #self.password = bcrypt.hash(password)
        password_encode = password.encode('utf-8')[:72]
        self.password = pbkdf2_sha256.hash(password_encode)
        
    def check_password(self, password: str) -> bool:
        #return bcrypt.verify(password, self.password)
        password_encode = password.encode('utf-8')[:72]
        return pbkdf2_sha256.hash(password_encode) == self.password
    
    def set_twofa_secret(self, secret: str):
        """Guarda el secreto TOTP cifrado"""
        self.twofa_secret = secret
    
    def verify_totp(self, code: str) -> bool:
        """Verifica código TOTP"""
        if not self.twofa_secret or not self.twofa_enabled:
            return False
        totp = pyotp.TOTP(self.twofa_secret)
        return totp.verify(code, valid_window=1)
    
    def enable_twofa(self, secret: str):
        """Habilita 2FA"""
        self.twofa_secret = secret
        self.twofa_enabled = True
    
    def disable_twofa(self):
        """Deshabilita 2FA"""
        self.twofa_secret = None
        self.twofa_enabled = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'twofa_enabled': self.twofa_enabled
        }