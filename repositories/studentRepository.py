from models.student import Student
from extensions import db
from datetime import datetime


class StudentRepository:
    
    @staticmethod
    def create(nombre: str, apellido_paterno: str, apellido_materno: str, matricula: str, correo: str) -> Student:
        """Crear un nuevo alumno"""
        student = Student(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            matricula=matricula,
            correo=correo
        )
        db.session.add(student)
        db.session.commit()
        return student
    
    @staticmethod
    def get_by_id(student_id: int) -> Student:
        """Obtener alumno por ID"""
        return Student.query.get(student_id)
    
    @staticmethod
    def get_all() -> list:
        """Obtener todos los alumnos"""
        return Student.query.all()
    
    @staticmethod
    def get_by_matricula(matricula: str) -> Student:
        """Obtener alumno por matrícula"""
        return Student.query.filter_by(matricula=matricula).first()
    
    @staticmethod
    def get_by_correo(correo: str) -> Student:
        """Obtener alumno por correo"""
        return Student.query.filter_by(correo=correo).first()
    
    @staticmethod
    def get_by_date_range(fecha_inicio: datetime = None, fecha_fin: datetime = None) -> list:
        """Obtener alumnos por rango de fechas de alta"""
        query = Student.query
        
        if fecha_inicio:
            query = query.filter(Student.fecha_alta >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(Student.fecha_alta <= fecha_fin)
        
        return query.all()
    
    @staticmethod
    def update(student_id: int, nombre: str = None, apellido_paterno: str = None, 
               apellido_materno: str = None, correo: str = None) -> Student:
        """Actualizar un alumno"""
        student = Student.query.get(student_id)
        if not student:
            return None
        
        if nombre:
            student.nombre = nombre
        if apellido_paterno:
            student.apellido_paterno = apellido_paterno
        if apellido_materno:
            student.apellido_materno = apellido_materno
        if correo:
            student.correo = correo
        
        db.session.commit()
        return student
    
    @staticmethod
    def delete(student_id: int) -> bool:
        """Eliminar un alumno"""
        student = Student.query.get(student_id)
        if not student:
            return False
        
        db.session.delete(student)
        db.session.commit()
        return True
