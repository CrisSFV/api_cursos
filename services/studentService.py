from repositories.studentRepository import StudentRepository
from models.student import Student
from datetime import datetime
import re


class StudentService:
    
    @staticmethod
    def validate_email(correo: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, correo) is not None
    
    @staticmethod
    def create_student(nombre: str, apellido_paterno: str, apellido_materno: str, 
                      matricula: str, correo: str) -> Student:
        """Crear un nuevo alumno"""
        # Validaciones
        if not nombre or nombre.strip() == '':
            raise ValueError('El nombre es obligatorio')
        
        if not apellido_paterno or apellido_paterno.strip() == '':
            raise ValueError('El apellido paterno es obligatorio')
        
        if not apellido_materno or apellido_materno.strip() == '':
            raise ValueError('El apellido materno es obligatorio')
        
        if not matricula or matricula.strip() == '':
            raise ValueError('La matrícula es obligatoria')
        
        if not correo or correo.strip() == '':
            raise ValueError('El correo es obligatorio')
        
        # Validar email
        if not StudentService.validate_email(correo):
            raise ValueError('El correo no tiene un formato válido')
        
        # Validar que la matrícula no exista
        existing_student = StudentRepository.get_by_matricula(matricula)
        if existing_student:
            raise ValueError(f'La matrícula "{matricula}" ya está registrada')
        
        # Validar que el correo no exista
        existing_email = StudentRepository.get_by_correo(correo)
        if existing_email:
            raise ValueError(f'El correo "{correo}" ya está registrado')
        
        return StudentRepository.create(nombre, apellido_paterno, apellido_materno, matricula, correo)
    
    @staticmethod
    def get_student(student_id: int) -> Student:
        """Obtener un alumno por ID"""
        student = StudentRepository.get_by_id(student_id)
        if not student:
            raise ValueError('El alumno no existe')
        return student
    
    @staticmethod
    def get_all_students() -> list:
        """Obtener todos los alumnos"""
        return StudentRepository.get_all()
    
    @staticmethod
    def update_student(student_id: int, nombre: str = None, apellido_paterno: str = None,
                      apellido_materno: str = None, correo: str = None) -> Student:
        """Actualizar un alumno"""
        student = StudentRepository.get_by_id(student_id)
        if not student:
            raise ValueError('El alumno no existe')
        
        # Validaciones
        if nombre and nombre.strip() == '':
            raise ValueError('El nombre no puede estar vacío')
        
        if apellido_paterno and apellido_paterno.strip() == '':
            raise ValueError('El apellido paterno no puede estar vacío')
        
        if apellido_materno and apellido_materno.strip() == '':
            raise ValueError('El apellido materno no puede estar vacío')
        
        if correo:
            if correo.strip() == '':
                raise ValueError('El correo no puede estar vacío')
            if not StudentService.validate_email(correo):
                raise ValueError('El correo no tiene un formato válido')
            
            # Verificar que el correo no esté en uso por otro alumno
            existing_email = StudentRepository.get_by_correo(correo)
            if existing_email and existing_email.id != student_id:
                raise ValueError(f'El correo "{correo}" ya está registrado')
        
        return StudentRepository.update(student_id, nombre, apellido_paterno, apellido_materno, correo)
    
    @staticmethod
    def delete_student(student_id: int) -> bool:
        """Eliminar un alumno"""
        student = StudentRepository.get_by_id(student_id)
        if not student:
            raise ValueError('El alumno no existe')
        
        return StudentRepository.delete(student_id)
    
    @staticmethod
    def filter_students_by_date(fecha_inicio: str = None, fecha_fin: str = None) -> list:
        """Filtrar alumnos por rango de fechas de alta"""
        fecha_inicio_dt = None
        fecha_fin_dt = None
        
        # Convertir strings a datetime
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Formato de fecha_inicio inválido. Use YYYY-MM-DD')
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                # Agregar un día para incluir toda la fecha final
                fecha_fin_dt = datetime(fecha_fin_dt.year, fecha_fin_dt.month, fecha_fin_dt.day, 23, 59, 59)
            except ValueError:
                raise ValueError('Formato de fecha_fin inválido. Use YYYY-MM-DD')
        
        return StudentRepository.get_by_date_range(fecha_inicio_dt, fecha_fin_dt)
