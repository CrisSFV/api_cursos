# Instrucciones de Configuración Inicial

## 1. Preparar el Entorno

```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Linux/Mac
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configurar Base de Datos

### Opción A: Usar MySQL

Editar archivo `.env`:
```
DATABASE_URI=mysql://tu_usuario:tu_contraseña@localhost:3306/api_db
FLASK_ENV=development
SECRET_KEY=clave-super-secreta-aqui
JWT_SECRET_KEY=clave-jwt-aqui
```

**Crear la base de datos en MySQL:**
```sql
CREATE DATABASE api_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Opción B: Usar SQLite (Desarrollo Rápido)

Editar archivo `.env`:
```
DATABASE_URI=sqlite:///db.sqlite3
FLASK_ENV=development
SECRET_KEY=clave-super-secreta-aqui
JWT_SECRET_KEY=clave-jwt-aqui
```

## 3. Crear Tablas

```bash
# Primera vez
flask db upgrade

# O si necesitas crear desde cero:
flask db migrate -m "Crear tablas"
flask db upgrade
```

## 4. Ejecutar la Aplicación

```bash
python app.py
```

La API estará disponible en: `http://localhost:5000`

Documentación Swagger: `http://localhost:5000/apidocs`

## 5. Probar Endpoints

### Crear una categoría
```bash
curl -X POST http://localhost:5000/api/v1/categorias \
  -H "Content-Type: application/json" \
  -d '{"name":"Programación","description":"Cursos de programación"}'
```

### Crear un curso
```bash
curl -X POST http://localhost:5000/api/v1/cursos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Python Básico",
    "descripcion":"Aprende los fundamentos de Python",
    "precio":49.99,
    "categoria_id":1
  }'
```

## Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error de conexión a base de datos
- Verificar que la base de datos está corriendo
- Verificar las credenciales en `.env`
- Verificar el formato de `DATABASE_URI`

### Error en migraciones
```bash
# Resetear migraciones (cuidado, borra datos)
rm -rf migrations/versions/*
flask db migrate -m "Reset"
flask db upgrade
```
