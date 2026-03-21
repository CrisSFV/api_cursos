from models.category import Category
from extensions import db


class CategoryRepository:
    
    @staticmethod
    def create(name: str, description: str = None) -> Category:
        """Crear una nueva categoría"""
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def get_by_id(category_id: int) -> Category:
        """Obtener categoría por ID"""
        return Category.query.get(category_id)
    
    @staticmethod
    def get_all() -> list:
        """Obtener todas las categorías"""
        return Category.query.all()
    
    @staticmethod
    def get_by_name(name: str) -> Category:
        """Obtener categoría por nombre"""
        return Category.query.filter_by(name=name).first()
    
    @staticmethod
    def update(category_id: int, name: str = None, description: str = None) -> Category:
        """Actualizar una categoría"""
        category = Category.query.get(category_id)
        if not category:
            return None
        
        if name:
            category.name = name
        if description:
            category.description = description
        
        db.session.commit()
        return category
    
    @staticmethod
    def delete(category_id: int) -> bool:
        """Eliminar una categoría"""
        category = Category.query.get(category_id)
        if not category:
            return False
        
        db.session.delete(category)
        db.session.commit()
        return True
