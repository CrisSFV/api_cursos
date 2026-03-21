from repositories.categoryRepository import CategoryRepository
from models.category import Category


class CategoryService:
    
    @staticmethod
    def create_category(name: str, description: str = None) -> Category:
        """Crear una nueva categoría"""
        # Validar que el nombre no esté vacío
        if not name or name.strip() == '':
            raise ValueError('El nombre de la categoría es obligatorio')
        
        # Validar que la categoría no exista
        existing_category = CategoryRepository.get_by_name(name)
        if existing_category:
            raise ValueError(f'La categoría "{name}" ya existe')
        
        return CategoryRepository.create(name, description)
    
    @staticmethod
    def get_category(category_id: int) -> Category:
        """Obtener una categoría por ID"""
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise ValueError('La categoría no existe')
        return category
    
    @staticmethod
    def get_all_categories() -> list:
        """Obtener todas las categorías"""
        return CategoryRepository.get_all()
    
    @staticmethod
    def update_category(category_id: int, name: str = None, description: str = None) -> Category:
        """Actualizar una categoría"""
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise ValueError('La categoría no existe')
        
        if name and name.strip() == '':
            raise ValueError('El nombre de la categoría no puede estar vacío')
        
        return CategoryRepository.update(category_id, name, description)
    
    @staticmethod
    def delete_category(category_id: int) -> bool:
        """Eliminar una categoría"""
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise ValueError('La categoría no existe')
        
        return CategoryRepository.delete(category_id)
