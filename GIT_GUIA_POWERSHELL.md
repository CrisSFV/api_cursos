# 🚀 GUÍA RÁPIDA: SUBIR A GITHUB

## 1️⃣ Configuración Inicial de Git (Una sola vez)

```powershell
# Configurar usuario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Verificar configuración
git config --global --list
```

## 2️⃣ Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. **Repository name:** `api_cursos`
3. **Description:** `API REST para gestionar cursos y categorías`
4. **Visibility:** Seleccionar "Public" o "Private"
5. **NO INICIALIZAR** con README (ya tenemos uno)
6. Click en **"Create repository"**

GitHub mostrará las instrucciones. Seguir los pasos del 3️⃣ abajo.

## 3️⃣ Inicializar Repositorio Local

```powershell
# Navegar a la carpeta
cd C:\Users\crist\ProyectoRich\api_ing_82

# Inicializar git
git init

# Ver estado (todos los archivos mostrarán como "Untracked")
git status
```

## 4️⃣ Hacer Primer Commit

```powershell
# Agregar todos los archivos
git add .

# Ver cambios staged
git status

# Hacer commit con mensaje
git commit -m "Inicializar: CRUD de cursos con Swagger"

# Ver log
git log
```

## 5️⃣ Conectar con GitHub

Reemplazar `USUARIO` con tu usuario de GitHub y `REPO` con el nombre del repositorio:

```powershell
# Agregar remote (conexión a GitHub)
git remote add origin https://github.com/USUARIO/REPO.git

# Cambiar rama a main (si es necesario)
git branch -M main

# Verificar remote
git remote -v
```

## 6️⃣ Subir Cambios a GitHub

```powershell
# Subir cambios
git push -u origin main

# Cuando pida credenciales, usar:
# Usuario: Tu usuario de GitHub
# Contraseña: Tu token de acceso personal (PAT)
```

## 🔑 Autenticación en GitHub (Si Pide Contraseña)

### Opción A: Token Personal (Recomendado)

1. Ir a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Configurar:
   - **Note:** `PowerShell Token`
   - **Expiration:** 90 days (o tu preferencia)
   - **Scopes:** 
     - [ ] `repo` - Acceso a repositorios
     - [ ] `admin:repo_hook` - Permisos de webhooks
4. Click "Generate token"
5. **Copiar el token** (no se mostrará de nuevo)
6. En PowerShell, cuando pida contraseña, pegar el token

### Opción B: Configurar SSH (Más Seguro)

```powershell
# 1. Generar clave SSH
ssh-keygen -t ed25519 -C "tu@email.com"

# 2. Presionar Enter para ruta por defecto
# 3. Presionar Enter para sin contraseña (o agregar contraseña)

# 4. Ver la clave pública
cat $env:USERPROFILE\.ssh\id_ed25519.pub

# 5. Copiar salida completa

# 6. GitHub → Settings → SSH and GPG keys → New SSH key
#    Pegar la clave pública

# 7. Probar conexión
ssh -T git@github.com

# 8. Cambiar remoto a SSH
git remote set-url origin git@github.com:USUARIO/REPO.git

# 9. Subir cambios
git push -u origin main
```

## 📝 Flujo de Trabajo Diario

```powershell
# 1. Ver cambios
git status

# 2. Agregar tipos específicos de archivos (ejemplo)
git add models/
git add controllers/

# O agregar todo
git add .

# 3. Hacer commit con mensaje descriptivo
git commit -m "Agregar validación de errores en cursos"

# 4. Subir a GitHub
git push

# 5. Ver historial
git log --oneline
```

## 🌿 Trabajar con Ramas

```powershell
# Ver ramas locales
git branch

# Ver todas las ramas (incluyendo remotas)
git branch -a

# Crear nueva rama
git checkout -b feature/nueva-caracteristica

# Cambiar a rama
git checkout main

# Eliminar rama local
git branch -d feature/nueva-caracteristica

# Subir rama a GitHub
git push origin feature/nueva-caracteristica
```

## 🔄 Actualizar Local desde GitHub

```powershell
# Ver cambios en remoto
git fetch

# Actualizar rama actual
git pull

# Actualizar rama específica
git pull origin main
```

## ↩️ Deshacer Cambios

```powershell
# Ver cambios no staged
git diff

# Deshacer cambios en archivo específico
git checkout -- controllers/CourseController.py

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer y perder cambios últimos
git reset --hard HEAD~1

# Deshacer múltiples commits
git reset --soft HEAD~3
git commit -m "Agrupar últimos 3 commits"
```

## 🏷️ Crear Versiones (Tags)

```powershell
# Crear tag
git tag v1.0.0

# Subir tag a GitHub
git push origin v1.0.0

# Ver tags
git tag

# Crear tag anotado con mensaje
git tag -a v1.0.0 -m "Version 1.0.0 - CRUD de Cursos"
```

## 📊 Ver Historial

```powershell
# Ver log resumido
git log --oneline

# Ver últimos 5 commits
git log -5

# Ver cambios específicos
git log -p

# Ver gráfico de ramas
git log --graph --oneline --all

# Ver diferencias entre commits
git diff COMMIT_SHA_1 COMMIT_SHA_2
```

## ⚡ Comandos Úti les Rápidos

```powershell
# Ver estado actual
git status

# Ver remoto
git remote -v

# Agregar todos y commit en un comando
git add . && git commit -m "Mensaje"

# Descargar y aplicar cambios remotos
git pull

# Subir cambios
git push

# Ver últimos cambios
git log --oneline -10

# Ver quién editó última
git blame controllers/CourseController.py
```

## ❌ Problemas Comunes

### "Error: remote origin already exists"
```powershell
# Remover el remoto anterior
git remote remove origin

# Agregar el nuevo
git remote add origin https://github.com/USUARIO/REPO.git
```

### "error: Your local changes to the following files would be overwritten"
```powershell
# Ver cambios
git diff

# Stash (guardar cambios temporalmente)
git stash

# Aplicar cambios guardados
git stash pop
```

### "fatal: not a git repository"
```powershell
# Te encuentras en carpeta sin .git
# Navega a la carpeta correcta o ejecuta
git init
```

## 🎯 Checklist Final

- [ ] Archivo `.env` creado con credenciales
- [ ] Base de datos configurada y migraciones aplicadas
- [ ] API probada localmente funciona
- [ ] Repositorio creado en GitHub
- [ ] Git inicializado localmente
- [ ] Todos archivos agregados con `git add .`
- [ ] Primer commit hecho
- [ ] Remote agregado
- [ ] Cambios subidos con `git push`
- [ ] Repositorio visible en GitHub web

## 📚 Recursos Útiles

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)
- [Pro Git Book](https://git-scm.com/book/es/v2)

---

**¡Listo para compartir con el mundo! 🚀**
