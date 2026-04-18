# 🎓 API de Gestión de Cursos - Examen Técnico Backend 2

**Fecha:** 2026-04-18  
**Horario:** 08:40 - 12:40  
**Status:** 🚀 En Desarrollo - FASE 1 Completa

## 📋 Contenido

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Fases del Proyecto](#fases-del-proyecto)
- [Endpoints API](#endpoints-api)
- [Git Workflow](#git-workflow)
- [Despliegue](#despliegue)

---

## 📌 Descripción

API REST para la gestión de cursos y categorías con autenticación avanzada usando **JWT** y **AWS Cognito** (fase 2), desplegada en infraestructura de AWS.

### Objetivos
✅ Autenticación con JWT  
✅ CRUD de Cursos y Categorías  
✅ Filtros avanzados (categoría, fecha)  
✅ 2FA (TOTP)  
✅ Documentación Swagger/OpenAPI  
✅ CI/CD con GitLab  
✅ Containerización con Docker (Alpine)  
✅ Despliegue en AWS (EC2, RDS)  

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                      │
│                   AWS Amplify                           │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                    API Gateway                          │
│                  (AWS ALB/ELB)                          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              EC2 Instance (Docker)                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │    Python Flask + Gunicorn                      │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │    Controllers (Auth, Courses, etc)      │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │    Services (Business Logic)             │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │    Repositories (Data Access)            │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              RDS Database (MySQL)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    users     │  │  categories  │  │    courses   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Tecnologías

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Backend** | Python | 3.11 |
| **Framework** | Flask | 3.0.3 |
| **BD** | MySQL/PostgreSQL | RDS |
| **Autenticación** | JWT + 2FA (TOTP) | 4.6.0 |
| **ORM** | SQLAlchemy | 2.0.31 |
| **Migraciones** | Alembic | 1.13.3 |
| **API Docs** | Swagger/Flasgger | 0.9.7.1 |
| **Servidor** | Gunicorn | 21.2.0 |
| **Containers** | Docker | Latest (Alpine) |
| **CI/CD** | GitLab | CI/CD Runners |
| **Cloud** | AWS | EC2, RDS, Lambda |

---

## 💾 Instalación

### Requisitos Previos
- Python 3.11+
- MySQL/PostgreSQL
- Docker
- Git
- AWS CLI (para despliegue)

### Paso 1: Clonar Repositorio

```bash
git clone https://gitlab.com/tu-repo/api-cursos.git
cd api-cursos
```

### Paso 2: Crear Entorno Virtual

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Editar .env con tus datos
nano .env
```

**Variables necesarias:**
```env
FLASK_ENV=development
DATABASE_URI=mysql+mysqldb://usuario:password@localhost:3306/cursos_db
SECRET_KEY=tu-clave-secreta
JWT_SECRET_KEY=tu-clave-jwt-secreta
```

### Paso 5: Crear Base de Datos

```bash
# Opción 1: Usando MySQL directamente
mysql -u usuario -p < scripts/setup_rds.sh

# Opción 2: Usando Flask CLI
python -c "from app import create_app; app=create_app(); app.app_context().push(); from extensions import db; db.create_all()"
```

### Paso 6: Ejecutar Aplicación

```bash
# Desarrollo
python app.py

# Con Gunicorn
gunicorn --bind 0.0.0.0:5000 app:create_app()
```

**La API estará disponible en:**
- 🌐 API: http://localhost:5000/api/v1
- 📚 Docs: http://localhost:5000/apidocs

---

## 📖 Uso

### Autenticación (JWT)

#### Registrar usuario
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_doe",
    "email": "juan@example.com",
    "password": "Password123!"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_doe",
    "password": "Password123!"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "juan_doe",
    "email": "juan@example.com",
    "twofa_enabled": false
  }
}
```

#### Usar Token en Endpoints Protegidos
```bash
curl -X GET http://localhost:5000/api/v1/cursos \
  -H "Authorization: Bearer <tu-token>"
```

### Gestión de Cursos

#### Crear Curso
```bash
curl -X POST http://localhost:5000/api/v1/cursos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Python Avanzado",
    "descripcion": "Aprende Python a nivel avanzado",
    "precio": 99.99,
    "categoria_id": 1
  }'
```

#### Obtener Cursos con Filtros
```bash
# Todos los cursos
curl http://localhost:5000/api/v1/cursos

# Filtrar por categoría
curl http://localhost:5000/api/v1/cursos?categoria=1

# Filtrar por fecha
curl http://localhost:5000/api/v1/cursos?fecha_inicio=2026-01-01&fecha_fin=2026-12-31

# Combinado
curl http://localhost:5000/api/v1/cursos?categoria=1&fecha_inicio=2026-01-01
```

---

## 🔄 Fases del Proyecto

### ✅ FASE 1: Core API (Completada)
- [x] Autenticación JWT
- [x] 2FA con TOTP
- [x] CRUD Cursos
- [x] CRUD Categorías
- [x] Filtros avanzados
- [x] Swagger/OpenAPI
- [x] Middleware de protección

### 🔄 FASE 2: AWS Cognito (En Progreso)
- [ ] Integración AWS Cognito
- [ ] Social login (Google, GitHub)
- [ ] Recuperación de contraseña
- [ ] Validación de email

### 🔄 FASE 3: Dockerización
- [x] Dockerfile (Alpine)
- [ ] Docker Compose
- [ ] Optimización de imagen

### 🔄 FASE 4: CI/CD
- [x] GitLab CI/CD Pipeline
- [x] Stage: test, build, deploy_dev, deploy_prod
- [ ] Integration tests

### 🔄 FASE 5: Despliegue AWS
- [x] Scripts de despliegue EC2
- [x] Scripts de setup RDS
- [ ] Infrastructure as Code (Terraform/Bicep)
- [ ] Monitoreo con CloudWatch

---

## 🔗 Endpoints API

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Registrar usuario |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refrescar token |
| GET | `/api/v1/auth/verify` | Verificar token |
| POST | `/api/v1/auth/2fa/enable-qr` | Generar QR 2FA |
| POST | `/api/v1/auth/2fa/enable` | Activar 2FA |
| POST | `/api/v1/auth/2fa/disable` | Desactivar 2FA |

### Cursos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/cursos` | Listar cursos |
| POST | `/api/v1/cursos` | Crear curso |
| GET | `/api/v1/cursos/{id}` | Obtener curso |
| PUT | `/api/v1/cursos/{id}` | Actualizar curso |
| DELETE | `/api/v1/cursos/{id}` | Eliminar curso |

### Categorías
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/categorias` | Listar categorías |
| POST | `/api/v1/categorias` | Crear categoría |
| GET | `/api/v1/categorias/{id}` | Obtener categoría |
| PUT | `/api/v1/categorias/{id}` | Actualizar categoría |
| DELETE | `/api/v1/categorias/{id}` | Eliminar categoría |

---

## 🌳 Git Workflow

### Ramas Principales
```
main (PROD)
  ├── hotfix/xxx
  └── release/x.x.x

develop (DEV)
  ├── feature/jwt-auth ✅
  ├── feature/cognito-auth 🔄
  ├── feature/deployment
  └── feature/cicd-pipeline ✅
```

### Crear Feature Branch
```bash
git checkout -b feature/mi-feature

# Hacer cambios...
git add .
git commit -m "feat: descripción de cambios"

# Push
git push origin feature/mi-feature

# Crear Merge Request en GitLab
```

### Merge a Develop
```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/mi-feature
git push origin develop
```

### Release a Main
```bash
git checkout main
git pull origin main
git merge --no-ff develop
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags
```

---

## 🚀 Despliegue

### Local con Docker
```bash
# Construir imagen
docker build -t api-cursos:latest .

# Ejecutar contenedor
docker run -d \
  --name api-cursos \
  -p 5000:5000 \
  --env-file .env \
  api-cursos:latest

# Ver logs
docker logs -f api-cursos
```

### En AWS EC2
```bash
# Usando script bash
bash scripts/deploy_ec2.sh 54.123.45.67

# O PowerShell
.\scripts\deploy_ec2.ps1 -EC2IP "54.123.45.67" -KeyPath "C:\path\to\key.pem"
```

### Setup RDS
```bash
bash scripts/setup_rds.sh \
  "db-cursos.cozu8wwe6bt6.us-east-1.rds.amazonaws.com" \
  "admin" \
  "password123" \
  "app_db"
```

---

## 📊 Testing

### Tests Unitarios
```bash
pytest tests/ -v
```

### Cobertura
```bash
pytest --cov=app tests/
```

---

## 🐛 Troubleshooting

### Problema: "No se puede conectar a BD"
```bash
# Verificar credenciales en .env
# Verificar que RDS esté accesible
mysql -h <host> -u <user> -p -e "SELECT 1"
```

### Problema: "Token inválido"
```bash
# Asegúrate de que JWT_SECRET_KEY sea el mismo
# Verifica el formato del header Authorization
Authorization: Bearer <token>
```

### Problema: Docker no construye
```bash
# Verificar que Alpine tenga deps necesarios
docker build --no-cache -t api-cursos:latest .

# Ver logs completos
docker build -t api-cursos:latest . 2>&1 | tail -50
```

---

## 📚 Documentación Adicional

- [Swagger/OpenAPI](http://localhost:5000/apidocs)
- [Git Workflow](./docs/git-workflow.md)
- [AWS Setup Guide](./docs/aws-setup.md)
- [Contributing](./CONTRIBUTING.md)

---

## 📝 Licencia

Este proyecto es parte del Examen Técnico Backend 2 (2026-04-18)

---

## 👤 Autor

**Cristian Fuentes**  
Estudiante de Ingeniería en Sistemas

---

**Última actualización:** 2026-04-18  
**Estado:** 🚀 En Desarrollo - FASE 1 Completada
