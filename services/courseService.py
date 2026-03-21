from repositories.courseRepository import CourseRepository
from repositories.categoryRepository import CategoryRepository
from models.course import Course
from datetime import datetime


class CourseService:
    
    @staticmethod
    def create_course(nombre: str, descripcion: str, precio: float, categoria_id: int) -> Course:
        """Crear un nuevo curso"""
        # Validaciones
        if not nombre or nombre.strip() == '':
            raise ValueError('El nombre del curso es obligatorio')
        
        if not descripcion or descripcion.strip() == '':
            raise ValueError('La descripción del curso es obligatoria')
        
        if precio <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        
        # Validar que la categoría exista
        category = CategoryRepository.get_by_id(categoria_id)
        if not category:
            raise ValueError(f'La categoría con ID {categoria_id} no existe')
        
        return CourseRepository.create(nombre, descripcion, precio, categoria_id)
    
    @staticmethod
    def get_course(course_id: int) -> Course:
        """Obtener un curso por ID"""
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError('El curso no existe')
        return course
    
    @staticmethod
    def get_all_courses() -> list:
        """Obtener todos los cursos"""
        return CourseRepository.get_all()
    
    @staticmethod
    def update_course(course_id: int, nombre: str = None, descripcion: str = None, precio: float = None, categoria_id: int = None) -> Course:
        """Actualizar un curso"""
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError('El curso no existe')
        
        # Validaciones
        if nombre and nombre.strip() == '':
            raise ValueError('El nombre del curso no puede estar vacío')
        
        if descripcion and descripcion.strip() == '':
            raise ValueError('La descripción del curso no puede estar vacía')
        
        if precio is not None and precio <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        
        if categoria_id:
            category = CategoryRepository.get_by_id(categoria_id)
            if not category:
                raise ValueError(f'La categoría con ID {categoria_id} no existe')
        
        return CourseRepository.update(course_id, nombre, descripcion, precio, categoria_id)
    
    @staticmethod
    def delete_course(course_id: int) -> bool:
        """Eliminar un curso"""
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError('El curso no existe')
        
        return CourseRepository.delete(course_id)
    
    @staticmethod
    def filter_courses(categoria_id: int = None, fecha_inicio: str = None, fecha_fin: str = None) -> list:
        """Filtrar cursos por categoría y/o rango de fechas"""
        fecha_inicio_dt = None
        fecha_fin_dt = None
        
        # Convertir strings a datetime
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f'Formato de fecha_inicio inválido. Use YYYY-MM-DD')
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                # Agregar un día para incluir toda la fecha final
                fecha_fin_dt = datetime(fecha_fin_dt.year, fecha_fin_dt.month, fecha_fin_dt.day, 23, 59, 59)
            except ValueError:
                raise ValueError(f'Formato de fecha_fin inválido. Use YYYY-MM-DD')
        
        return CourseRepository.filter_by_category_and_date(categoria_id, fecha_inicio_dt, fecha_fin_dt)
