#!/bin/bash
# Script de prueba de API - API de Cursos
# Ejecutar con: bash test_api_examples.sh

API_URL="http://localhost:5000/api/v1"
HEADER_JSON="Content-Type: application/json"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        EJEMPLOS DE PRUEBA - API DE CURSOS                 ║"
echo "╚════════════════════════════════════════════════════════════╝"

echo ""
echo "1️⃣  CREAR CATEGORÍA"
echo "---"
curl -X POST "$API_URL/categorias" \
  -H "$HEADER_JSON" \
  -d '{
    "name": "Programación",
    "description": "Cursos de lenguajes de programación"
  }' | python -m json.tool
echo ""

echo "2️⃣  CREAR SEGUNDA CATEGORÍA"
echo "---"
curl -X POST "$API_URL/categorias" \
  -H "$HEADER_JSON" \
  -d '{
    "name": "Diseño Web",
    "description": "Cursos de diseño y desarrollo web"
  }' | python -m json.tool
echo ""

echo "3️⃣  OBTENER TODAS LAS CATEGORÍAS"
echo "---"
curl -X GET "$API_URL/categorias" | python -m json.tool
echo ""

echo "4️⃣  CREAR UN CURSO (requiere categoria_id = 1)"
echo "---"
curl -X POST "$API_URL/cursos" \
  -H "$HEADER_JSON" \
  -d '{
    "nombre": "Python Básico",
    "descripcion": "Aprende los fundamentos de Python desde cero",
    "precio": 49.99,
    "categoria_id": 1
  }' | python -m json.tool
echo ""

echo "5️⃣  CREAR OTRO CURSO"
echo "---"
curl -X POST "$API_URL/cursos" \
  -H "$HEADER_JSON" \
  -d '{
    "nombre": "JavaScript Avanzado",
    "descripcion": "Domina JavaScript con ES6 y frameworks modernos",
    "precio": 79.99,
    "categoria_id": 2
  }' | python -m json.tool
echo ""

echo "6️⃣  OBTENER TODOS LOS CURSOS"
echo "---"
curl -X GET "$API_URL/cursos" | python -m json.tool
echo ""

echo "7️⃣  FILTRAR CURSOS POR CATEGORÍA (categoria=1)"
echo "---"
curl -X GET "$API_URL/cursos?categoria=1" | python -m json.tool
echo ""

echo "8️⃣  OBTENER UN CURSO POR ID (id=1)"
echo "---"
curl -X GET "$API_URL/cursos/1" | python -m json.tool
echo ""

echo "9️⃣  ACTUALIZAR UN CURSO (id=1)"
echo "---"
curl -X PUT "$API_URL/cursos/1" \
  -H "$HEADER_JSON" \
  -d '{
    "nombre": "Python Intermedio",
    "precio": 59.99
  }' | python -m json.tool
echo ""

echo "🔟  ACTUALIZAR UNA CATEGORÍA (id=1)"
echo "---"
curl -X PUT "$API_URL/categorias/1" \
  -H "$HEADER_JSON" \
  -d '{
    "name": "Programación Python",
    "description": "Cursos especializados de Python"
  }' | python -m json.tool
echo ""

echo "1️⃣1️⃣  FILTRAR CURSOS POR RANGO DE FECHAS"
echo "---"
echo "Format: /api/v1/cursos?categoria=1&fecha_inicio=2026-03-20&fecha_fin=2026-03-25"
echo "No se mostrarán resultados si no hay cursos creados en ese rango"
echo ""

echo "1️⃣2️⃣  ELIMINAR UN CURSO (id=1)"
echo "---"
curl -X DELETE "$API_URL/cursos/1"
echo ""

echo "1️⃣3️⃣  ELIMINAR UNA CATEGORÍA (id=2)"
echo "---"
curl -X DELETE "$API_URL/categorias/2"
echo ""

echo "✅ PRUEBAS COMPLETADAS"
echo ""
echo "📊 PARA VER LA DOCUMENTACIÓN SWAGGER:"
echo "http://localhost:5000/apidocs"
