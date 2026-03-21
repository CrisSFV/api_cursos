"# API de Cursos

API REST para gestionar cursos y categorías con operaciones CRUD completas.

## Características

- ✅ CRUD completo de cursos (Crear, Leer, Actualizar, Eliminar)
- ✅ CRUD completo de categorías
- ✅ Filtrado de cursos por categoría
- ✅ Filtrado de cursos por rango de fechas
- ✅ Documentación automática con Swagger
- ✅ Manejo de errores robusto
- ✅ Estructura modular (Controllers, Services, Repositories)

## Requisitos

- Python 3.8+
- MySQL (o cambiar la base de datos en `config.py`)

## Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <tu-repositorio>
cd api_ing_82

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env
# DATABASE_URI=mysql://usuario:contraseña@localhost/api_db
# SECRET_KEY=tu-clave-secreta
# JWT_SECRET_KEY=tu-jwt-secreto

# 5. Crear base de datos
flask db upgrade

# 6. Ejecutar
python app.py
```

## Estructura del Proyecto

```
api_ing_82/
├── app.py                    # Aplicación Flask principal
├── config.py                 # Configuración
├── extensions.py             # Extensiones (DB, JWT, Swagger)
├── requirements.txt          # Dependencias
├── controllers/              # Controladores de rutas
│   ├── CourseController.py   # Endpoints de cursos
│   └── CategoryController.py # Endpoints de categorías
├── services/                 # Lógica de negocio
│   ├── courseService.py
│   └── categoryService.py
├── repositories/             # Acceso a base de datos
│   ├── courseRepository.py
│   └── categoryRepository.py
├── models/                   # Modelos de datos
│   ├── course.py
│   └── category.py
└── migrations/               # Migraciones de base de datos
```

## Uso de la API

### Swagger (Documentación Interactiva)
```
http://localhost:5000/apidocs
```

### Endpoints Principales

#### Categorías
- `POST /api/v1/categorias` - Crear categoría
- `GET /api/v1/categorias` - Obtener todas
- `GET /api/v1/categorias/{id}` - Obtener por ID
- `PUT /api/v1/categorias/{id}` - Actualizar
- `DELETE /api/v1/categorias/{id}` - Eliminar

#### Cursos
- `POST /api/v1/cursos` - Crear curso
- `GET /api/v1/cursos` - Obtener todos
- `GET /api/v1/cursos?categoria=1&fecha_inicio=2026-03-20&fecha_fin=2026-03-25` - Filtrar
- `GET /api/v1/cursos/{id}` - Obtener por ID
- `PUT /api/v1/cursos/{id}` - Actualizar
- `DELETE /api/v1/cursos/{id}` - Eliminar

## Ejemplos

### Crear Categoría
```bash
curl -X POST http://localhost:5000/api/v1/categorias \
  -H "Content-Type: application/json" \
  -d '{"name":"Programación","description":"Cursos de programación"}'
```

### Crear Curso
```bash
curl -X POST http://localhost:5000/api/v1/cursos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Python Básico",
    "descripcion":"Aprende Python",
    "precio":49.99,
    "categoria_id":1
  }'
```

### Filtrar Cursos
```bash
curl "http://localhost:5000/api/v1/cursos?categoria=1&fecha_inicio=2026-03-20&fecha_fin=2026-03-25"
```

## Licencia

MIT