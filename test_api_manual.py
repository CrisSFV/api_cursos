#!/usr/bin/env python
"""
Script de prueba para la API - Alternativa a Swagger UI
Usa requests para probar todos los endpoints
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000/api/v1"
TOKEN = None

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, method, endpoint):
    """Print test header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}📍 TEST: {name}{Colors.ENDC}")
    print(f"   {Colors.YELLOW}{method} {endpoint}{Colors.ENDC}")

def print_success(status, data):
    """Print success response"""
    print(f"   {Colors.GREEN}✅ Status: {status}{Colors.ENDC}")
    print(f"   {Colors.BLUE}📤 Response:{Colors.ENDC}")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    return data

def print_error(status, error):
    """Print error response"""
    print(f"   {Colors.RED}❌ Status: {status}{Colors.ENDC}")
    print(f"   {Colors.RED}Error: {error}{Colors.ENDC}")
    return None

def test_register():
    """Test: Registrar usuario"""
    global TOKEN
    
    print_test("Registrar Usuario", "POST", "/auth/register")
    
    payload = {
        "username": f"test_user_{datetime.now().timestamp()}",
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "TestPassword123!"
    }
    
    print(f"   📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(response.status_code, data)
            return payload["username"], payload["password"], data.get("id")
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

def test_login(username, password):
    """Test: Login"""
    global TOKEN
    
    print_test("Login", "POST", "/auth/login")
    
    payload = {
        "username": username,
        "password": password
    }
    
    print(f"   📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get("access_token")
            print_success(response.status_code, data)
            print(f"\n   {Colors.GREEN}✅ Token obtenido: {TOKEN[:50]}...{Colors.ENDC}")
            return TOKEN
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

def test_create_category(token):
    """Test: Crear categoría"""
    print_test("Crear Categoría", "POST", "/categorias")
    
    payload = {
        "name": f"Categoría Test {datetime.now().timestamp()}",
        "description": "Categoría de prueba"
    }
    
    print(f"   📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/categorias",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(response.status_code, data)
            return data.get("id")
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

def test_create_course(token, category_id):
    """Test: Crear curso"""
    print_test("Crear Curso", "POST", "/cursos")
    
    payload = {
        "nombre": f"Curso Test {datetime.now().timestamp()}",
        "descripcion": "Este es un curso de prueba",
        "precio": 99.99,
        "categoria_id": category_id
    }
    
    print(f"   📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/cursos",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(response.status_code, data)
            return data.get("id")
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

def test_get_courses(token):
    """Test: Obtener todos los cursos"""
    print_test("Obtener Cursos", "GET", "/cursos")
    
    try:
        response = requests.get(
            f"{BASE_URL}/cursos",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(response.status_code, {"total_cursos": len(data), "cursos": data[:2]})
            return data
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

def test_get_categories():
    """Test: Obtener categorías"""
    print_test("Obtener Categorías", "GET", "/categorias")
    
    try:
        response = requests.get(f"{BASE_URL}/categorias")
        
        if response.status_code == 200:
            data = response.json()
            print_success(response.status_code, {"total_categorias": len(data), "categorias": data[:2]})
            return data
        else:
            print_error(response.status_code, response.text)
            return None
    except Exception as e:
        print_error("ERROR", str(e))
        return None

# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}")
    print("🧪 TEST MANUAL - API de Cursos")
    print(f"{'='*50}{Colors.ENDC}\n")
    
    # Verificar que la API está disponible
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/")
        print(f"{Colors.GREEN}✅ API disponible en {BASE_URL}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ API no disponible: {e}{Colors.ENDC}")
        sys.exit(1)
    
    # Tests
    print(f"\n{Colors.BOLD}{Colors.CYAN}═ PRUEBA 1: AUTENTICACIÓN{Colors.ENDC}\n")
    
    result = test_register()
    if result:
        username, password, user_id = result
        token = test_login(username, password)
        
        if token:
            print(f"\n{Colors.BOLD}{Colors.CYAN}═ PRUEBA 2: CREAR CATEGORÍA Y CURSO{Colors.ENDC}\n")
            
            category_id = test_create_category(token)
            
            if category_id:
                course_id = test_create_course(token, category_id)
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}═ PRUEBA 3: OBTENER DATOS{Colors.ENDC}\n")
            
            test_get_courses(token)
            test_get_categories()
    
    # Resumen
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}")
    print("✅ TESTING COMPLETADO")
    print(f"{'='*50}{Colors.ENDC}\n")
    
    print(f"{Colors.GREEN}📚 Documentación Swagger: http://localhost:5000/apidocs{Colors.ENDC}\n")
