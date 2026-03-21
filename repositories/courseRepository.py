from models.course import Course
from extensions import db
from datetime import datetime


class CourseRepository:
    
    @staticmethod
    def create(nombre: str, descripcion: str, precio: float, categoria_id: int) -> Course:
        """Crear un nuevo curso"""
        course = Course(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria_id=categoria_id
        )
        db.session.add(course)
        db.session.commit()
        return course
    
    @staticmethod
    def get_by_id(course_id: int) -> Course:
        """Obtener curso por ID"""
        return Course.query.get(course_id)
    
    @staticmethod
    def get_all() -> list:
        """Obtener todos los cursos"""
        return Course.query.all()
    
    @staticmethod
    def get_by_category(categoria_id: int) -> list:
        """Obtener cursos por categoría"""
        return Course.query.filter_by(categoria_id=categoria_id).all()
    
    @staticmethod
    def get_by_date_range(fecha_inicio: datetime = None, fecha_fin: datetime = None) -> list:
        """Obtener cursos por rango de fechas"""
        query = Course.query
        
        if fecha_inicio:
            query = query.filter(Course.fecha_creacion >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(Course.fecha_creacion <= fecha_fin)
        
        return query.all()
    
    @staticmethod
    def filter_by_category_and_date(categoria_id: int = None, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> list:
        """Filtrar cursos por categoría y/o rango de fechas"""
        query = Course.query
        
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        
        if fecha_inicio:
            query = query.filter(Course.fecha_creacion >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(Course.fecha_creacion <= fecha_fin)
        
        return query.all()
    
    @staticmethod
    def update(course_id: int, nombre: str = None, descripcion: str = None, precio: float = None, categoria_id: int = None) -> Course:
        """Actualizar un curso"""
        course = Course.query.get(course_id)
        if not course:
            return None
        
        if nombre:
            course.nombre = nombre
        if descripcion:
            course.descripcion = descripcion
        if precio is not None:
            course.precio = precio
        if categoria_id:
            course.categoria_id = categoria_id
        
        db.session.commit()
        return course
    
    @staticmethod
    def delete(course_id: int) -> bool:
        """Eliminar un curso"""
        course = Course.query.get(course_id)
        if not course:
            return False
        
        db.session.delete(course)
        db.session.commit()
        return True
