#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para probar los endpoints de la API"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_home():
    print("\n" + "="*50)
    print("📍 Probando endpoint HOME")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_swagger():
    print("\n" + "="*50)
    print("📚 Probando Swagger UI")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/apidocs/")
        print(f"Status: {response.status_code}")
        print(f"✓ Swagger está disponible en: {BASE_URL}/apidocs/")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_register():
    print("\n" + "="*50)
    print("📝 Probando endpoint REGISTER")
    print("="*50)
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🚀 PROBANDO LA API")
    test_home()
    test_swagger()
    test_register()
    print("\n" + "="*50)
    print("✅ Pruebas completadas")
    print("="*50)
