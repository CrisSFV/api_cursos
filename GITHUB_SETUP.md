# Instrucciones para Subir a GitHub

## 1. Crear un proyecto en GitHub

1. Ir a https://github.com/new
2. Nombre: `api_cursos` (o el que prefieras)
3. Descripción: `API REST para gestionar cursos y categorías`
4. Seleccionar "Private" o "Public" según prefieras
5. NO inicializar con README (ya lo tenemos)
6. Click en "Create repository"

## 2. Configurar Git en Local

```bash
# Si no has configurado Git antes
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## 3. Inicializar Repositorio Local

```bash
cd c:\Users\crist\ProyectoRich\api_ing_82

# Inicializar git
git init

# Agregar todos los archivos
git add .

# Hacer primer commit
git commit -m "Commit inicial: CRUD de cursos con Swagger"
```

## 4. Conectar con GitHub

```bash
# Reemplazar USER con tu usuario de GitHub y REPO con el nombre del repositorio
git remote add origin https://github.com/USER/REPO.git

# Cambiar rama a main (si es necesario)
git branch -M main

# Subir los cambios
git push -u origin main
```

## 5. Si GitHub Pide Autenticación

### Opción A: Token Personal (Recomendado)

1. Ir a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generar nuevo token con permisos: `repo`, `user`, `admin:repo_hook`
3. Copiar el token
4. En PowerShell, cuando pida contraseña, pegar el token

### Opción B: Configurar SSH (Más Seguro)

```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu@email.com"

# Cuando pida ruta, presionar Enter
# Cuando pida contraseña, presionar Enter (o agregar una)

# Copiar la clave pública
cat $env:USERPROFILE\.ssh\id_ed25519.pub

# Ir a GitHub → Settings → SSH and GPG keys → New SSH key
# Pegar la clave pública

# Probar conexión
ssh -T git@github.com

# Cambiar remoto a SSH
git remote set-url origin git@github.com:USER/REPO.git
```

## 6. Flujo de Trabajo Git

### Hacer cambios

```bash
# Ver estado
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción clara del cambio"

# Subir cambios
git push origin main
```

### Crear rama para nuevas features

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nueva-feature

# Hacer cambios y commits...

# Subir la rama
git push origin feature/nueva-feature

# Crear Pull Request en GitHub web
```

## 7. Crear .gitignore (Ya Existe)

El archivo `.gitignore` ya está creado y contiene:
- `.venv/` - Entorno virtual
- `__pycache__/` - Archivos compilados
- `.env` - Variables de entorno
- `*.log` - Archivos de log
- Archivos temporales

## 8. Estructura Final del Repositorio

```
api_ing_82/
├── README.md              # Documentación principal
├── SETUP.md               # Instrucciones de setup
├── GITHUB_SETUP.md        # Este archivo
├── ARQUITECTURA.puml      # Diagrama de arquitectura
├── .gitignore             # Archivos a ignorar
├── .env.example           # Ejemplo de variables
├── requirements.txt       # Dependencias Python
├── app.py                 # Aplicación principal
├── config.py              # Configuración
├── extensions.py          # Extensiones (DB, JWT, etc)
├── controllers/
│   ├── CourseController.py
│   └── CategoryController.py
├── models/
│   ├── course.py
│   └── category.py
├── services/
│   ├── courseService.py
│   └── categoryService.py
├── repositories/
│   ├── courseRepository.py
│   └── categoryRepository.py
└── migrations/            # Migraciones de BD
```

## 9. Opciones de Depósito

### GitHub (Recomendado - Gratuito)
- Repositorios públicos: Sin límite
- Repositorios privados: Sin límite
- Colaboradores: Sin límite
- CI/CD: GitHub Actions (gratuito)

### GitLab (Alternativa)
- Similar a GitHub
- Más espacio para runners CI/CD
- Interface más moderna

### Bitbucket (Otra alternativa)
- Gratis para equipos pequeños
- Integración con Jira
- Pipelines CI/CD incluidos

## 10. Comandos Útiles

```bash
# Ver historial de commits
git log --oneline

# Ver cambios no enviados
git diff

# Deshacer último commit (sin perder cambios)
git reset --soft HEAD~1

# Deshacer cambios de un archivo específico
git checkout -- archivo.py

# Crear tag (versión)
git tag v1.0.0
git push origin v1.0.0
```

## 11. Próximos Pasos

1. Actualizar código en local
2. Hacer commit: `git commit -m "mensaje"`
3. Subir: `git push origin main`
4. En GitHub, ir a la sección "Releases" y crear releases cuando suba de versión

## 12. Colaboración

Si otros van a trabajar en el proyecto:

```bash
# Clonar el repositorio
git clone https://github.com/USER/REPO.git

# Crear rama para feature
git checkout -b feature/nueva-feature

# Después de cambios
git push origin feature/nueva-feature

# Crear Pull Request en GitHub
```

Un miembro del equipo revisará y aprobará el PR antes de mergear con main.

## Preguntas Frecuentes

### ¿Qué es un Pull Request?
Es una solicitud para mergear cambios de una rama a otra. Permite revisión de código antes de integrar.

### ¿Cómo actualizo mi repositorio local?
```bash
git pull origin main
```

### ¿Qué hago si hay conflictos?
Los conflictos ocurren cuando dos branches modifican la misma línea. Git te mostrará dónde están y debes elegir qué mantener.

## Ayuda Adicional

- [GitHub Documentation](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Pro Git Book](https://git-scm.com/book/es/v2)
