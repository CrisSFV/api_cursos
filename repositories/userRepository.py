from models.user import User
from extensions import db

class UserRepository:
    @staticmethod
    def create(username,email,password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def save(user):
        """Guarda cambios del usuario en la BD"""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
