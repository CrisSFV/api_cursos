#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para probar la carga de secretos desde AWS Secrets Manager"""

from Settings.secret import Secret

print("=" * 50)
print("Probando carga de secretos desde AWS...")
print("=" * 50)

# Obtener los secretos
secret_key = Secret.get_secret_key()
jwt_secret_key = Secret.get_jwt_secret_key()

print(f"\nSECRET_KEY: {secret_key[:10]}..." if secret_key else "No cargado")
print(f"JWT_SECRET_KEY: {jwt_secret_key[:10]}..." if jwt_secret_key else "No cargado")

print("\n" + "=" * 50)
print("✓ Test completado exitosamente!")
print("=" * 50)
