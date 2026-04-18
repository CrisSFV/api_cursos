# Phase 2: React Frontend con AWS Amplify

## Requisitos Previos
- ✅ AWS Lambda (`holaLambda`) funcionando
- ✅ API Gateway REST API (`or9112xy9d`) funcionando
- ✅ Endpoints DES y PROD respondiendo correctamente

## Estructura del Proyecto
```
src/
  ├── App.jsx         # Componente principal React
  ├── App.css         # Estilos personalizados
  └── index.js        # Punto de entrada
public/
  └── index.html      # HTML base
package.json          # Dependencias de npm
```

## Pasos para Ejecutar Localmente

### 1. Instalar dependencias
```bash
npm install
```

### 2. Iniciar servidor de desarrollo
```bash
npm start
```
El servidor abrirá automáticamente en `http://localhost:3000`

### 3. Verificar funcionamiento
- Haz click en el botón **🔵 Dev** → debe mostrar "Hola dev"
- Haz click en el botón **🟢 Prod** → debe mostrar "Hola prod"

## Desplegar con AWS Amplify

### Opción A: Amplify Console (Web UI)
1. Conectar repositorio GitHub a Amplify Console
2. Seleccionar esta carpeta como raíz del proyecto
3. Configurar build settings:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - npm install
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: build
       files:
         - '**/*'
     cache:
       paths:
         - node_modules/**/*
   ```
4. Deploy automático en cada push

### Opción B: Amplify CLI (Terminal)
```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Inicializar Amplify Project
amplify init
# Seleccionar: React, JavaScript, npm, etc.

# Agregar hosting
amplify add hosting
# Seleccionar: Amplify Console, AWS CodeBuild

# Deploy
amplify publish
```

## Variables de Entorno

Si necesitas cambiar la URL de API Gateway, edita `src/App.jsx`:

```javascript
const API_BASE_URL = "https://or9112xy9d.execute-api.us-east-1.amazonaws.com";
```

O usa variables de entorno:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || "https://or9112xy9d.execute-api.us-east-1.amazonaws.com";
```

Luego crea archivo `.env`:
```
REACT_APP_API_URL=https://or9112xy9d.execute-api.us-east-1.amazonaws.com
```

## CORS en Lambda API Gateway

Si recibes errores de CORS, asegúrate que Lambda devuelve headers CORS:

```python
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"mensaje": "Hola desde stage"})
    }
```

## Arquitectura Final

```
┌─────────────┐
│   React UI  │  ← Amplify Hosting
│  (AWS)      │
└──────┬──────┘
       │ HTTP GET
       ▼
┌─────────────────────┐
│  API Gateway        │  ← REST API
│  /dev & /prod       │
└──────────┬──────────┘
           │ Invoke
           ▼
    ┌───────────────┐
    │  Lambda       │  ← holaLambda
    │  holaLambda   │  ← Python 3.11
    └───────────────┘
```

## Próximos Pasos

- [ ] Ejecutar `npm install`
- [ ] Ejecutar `npm start` para pruebas locales
- [ ] Desplegar con Amplify Console o CLI
- [ ] Verificar endpoints funcionan en producción

¡Listo! 🚀
