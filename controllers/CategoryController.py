from flask import Blueprint, request, jsonify
from services.categoryService import CategoryService
from flasgger import swag_from

category_bp = Blueprint('categories', __name__)


@category_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Categorías'],
    'summary': 'Crear una nueva categoría',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nombre de la categoría',
                        'example': 'Programación'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Descripción de la categoría (opcional)',
                        'example': 'Cursos de lenguajes de programación'
                    }
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Categoría creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'created_at': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Error en los datos enviados'
        }
    }
})
def create_category():
    """Crear una nueva categoría"""
    data = request.get_json() or {}
    
    try:
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({'error': 'El campo "name" es obligatorio'}), 400
        
        category = CategoryService.create_category(name, description)
        return jsonify(category.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear la categoría'}), 500


@category_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Categorías'],
    'summary': 'Obtener todas las categorías',
    'responses': {
        200: {
            'description': 'Lista de categorías',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'created_at': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_all_categories():
    """Obtener todas las categorías"""
    try:
        categories = CategoryService.get_all_categories()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener las categorías'}), 500


@category_bp.route('/<int:category_id>', methods=['GET'])
@swag_from({
    'tags': ['Categorías'],
    'summary': 'Obtener una categoría por ID',
    'parameters': [
        {
            'name': 'category_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la categoría'
        }
    ],
    'responses': {
        200: {
            'description': 'Categoría encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'created_at': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Categoría no encontrada'
        }
    }
})
def get_category(category_id):
    """Obtener una categoría por ID"""
    try:
        category = CategoryService.get_category(category_id)
        return jsonify(category.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener la categoría'}), 500


@category_bp.route('/<int:category_id>', methods=['PUT'])
@swag_from({
    'tags': ['Categorías'],
    'summary': 'Actualizar una categoría',
    'parameters': [
        {
            'name': 'category_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la categoría'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nuevo nombre'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Nueva descripción'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Categoría actualizada'
        },
        404: {
            'description': 'Categoría no encontrada'
        }
    }
})
def update_category(category_id):
    """Actualizar una categoría"""
    data = request.get_json() or {}
    
    try:
        name = data.get('name')
        description = data.get('description')
        
        category = CategoryService.update_category(category_id, name, description)
        return jsonify(category.to_dict()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al actualizar la categoría'}), 500


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Categorías'],
    'summary': 'Eliminar una categoría',
    'parameters': [
        {
            'name': 'category_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la categoría'
        }
    ],
    'responses': {
        200: {
            'description': 'Categoría eliminada exitosamente'
        },
        404: {
            'description': 'Categoría no encontrada'
        }
    }
})
def delete_category(category_id):
    """Eliminar una categoría"""
    try:
        CategoryService.delete_category(category_id)
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar la categoría'}), 500
