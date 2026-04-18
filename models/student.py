from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hashea la contraseña"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'matricula': self.matricula,
            'correo': self.correo,
            'fecha_alta': self.fecha_alta.isoformat() if self.fecha_alta else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
