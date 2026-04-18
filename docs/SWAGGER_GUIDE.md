# 📚 Cómo Usar Swagger (OpenAPI)

## 🌐 Acceder a Swagger

Abre en tu navegador:
```
http://localhost:5000/apidocs
```

---

## 📝 Cómo Enviar Datos en Swagger

### **Paso 1: Expandir un Endpoint POST**
Haz clic en cualquier endpoint **POST** (ej: `POST /auth/register`)

### **Paso 2: Click en "Try it out"**
Verás un botón **azul** con texto "Try it out" en la esquina derecha

### **Paso 3: Llenar el Formulario**
- Verás un editor de **JSON**
- **Reemplaza** el contenido con tus datos

**Ejemplo para POST /auth/register:**
```json
{
  "username": "juan_doe",
  "email": "juan@example.com",
  "password": "Password123!"
}
```

### **Paso 4: Click en "Execute"**
El botón de **Execute** enviará la solicitud

### **Paso 5: Ver Respuesta**
Debajo verás la respuesta con:
- ✅ Status Code
- 📤 Response Body
- 📋 Response Headers

---

## 🔐 Usar JWT Token en Swagger

### **Después de Login:**

1. Copia el `access_token` de la respuesta
2. En la esquina superior derecha, hay un botón **"Authorize"** 🔒
3. Selecciona **"BearerAuth"**
4. Pega tu token:
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
5. Click **"Authorize"**
6. Ahora todos los requests incluirán el token automáticamente

---

## 🧪 Problemas Comunes

### ❌ "Error sending request"
- **Solución:** Verifica que el JSON sea válido
- Usa un validador JSON: https://jsonlint.com/

### ❌ "401 Unauthorized"
- **Solución:** El token no es válido
- Vuelve a hacer login
- Copia el nuevo token y authorízate de nuevo

### ❌ "400 Bad Request"
- **Solución:** Falta algún campo requerido
- Verifica que todos los campos "required" estén presentes

### ❌ No se envía el JSON
- **Solución:** Asegúrate de:
  1. Hacer click en "Try it out"
  2. El JSON esté dentro del editor
  3. No hay errores de sintaxis JSON

---

## 📊 Flujo Típico de Testing

### 1️⃣ **Registrar Usuario**
```
POST /auth/register
{
  "username": "tu_usuario",
  "email": "tu@email.com",
  "password": "Password123!"
}
```
Copia el `id` de la respuesta

### 2️⃣ **Login**
```
POST /auth/login
{
  "username": "tu_usuario",
  "password": "Password123!"
}
```
Copia el `access_token`

### 3️⃣ **Autorizar en Swagger**
- Click en **Authorize** 🔒
- Pega: `Bearer <tu-access-token>`

### 4️⃣ **Crear Categoría**
```
POST /categorias
{
  "name": "Programación",
  "description": "Cursos de programación"
}
```
Copia el `id` de la categoría

### 5️⃣ **Crear Curso**
```
POST /cursos
{
  "nombre": "Python Avanzado",
  "descripcion": "Aprende Python a nivel avanzado",
  "precio": 99.99,
  "categoria_id": 1
}
```

### 6️⃣ **Obtener Cursos**
```
GET /cursos
```

---

## 💡 Alternativa: Script Python

Si Swagger no funciona bien, puedes usar el script manual:

```powershell
pip install requests
python test_api_manual.py
```

Este script probará todos los endpoints automáticamente y mostrará las respuestas.

---

## 🔗 URLs Útiles

- **API Base:** http://localhost:5000/api/v1
- **Swagger UI:** http://localhost:5000/apidocs
- **API Spec (JSON):** http://localhost:5000/apispec.json
- **Root:** http://localhost:5000/

---

## 📖 Documentación OpenAPI

La especificación OpenAPI 2.0 (Swagger) está disponible en:
```
http://localhost:5000/apispec.json
```

Puedes importarla en:
- **Postman:** https://www.postman.com/
- **Insomnia:** https://insomnia.rest/
- **REST Client (VS Code):** https://marketplace.visualstudio.com/items?itemName=humao.rest-client

---

**¿Necesitas ayuda?** 👇
