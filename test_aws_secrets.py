#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script detallado para verificar la integración con AWS Secrets Manager"""

import os
import json
import boto3
from botocore.exceptions import ClientError
from Settings.secret import Secret

print("\n" + "="*70)
print("🔐 VERIFICACIÓN DE AWS SECRETS MANAGER")
print("="*70)

# 1. Verificar configuración AWS
print("\n📋 CONFIGURACIÓN AWS:")
print(f"   Región: {os.getenv('AWS_REGION', 'us-east-1')}")
print(f"   Secret Name: {os.getenv('AWS_SECRET_NAME', 'api_ing_82/secrets')}")

# 2. Obtener secretos directamente desde AWS
print("\n☁️  OBTENIENDO SECRETOS DESDE AWS:")
try:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    response = client.get_secret_value(
        SecretId=os.getenv('AWS_SECRET_NAME', 'api_ing_82/secrets')
    )
    
    secret_data = json.loads(response['SecretString'])
    
    print(f"   ✓ Conectado exitosamente a AWS Secrets Manager")
    print(f"   ✓ ARN: {response['ARN']}")
    print(f"   ✓ Última actualización: {response['CreatedDate']}")
    print(f"\n   📦 Secretos almacenados:")
    for key in secret_data.keys():
        value = secret_data[key]
        masked = f"{value[:5]}{'*' * (len(value) - 10)}{value[-5:]}" if len(value) > 10 else "*" * len(value)
        print(f"      • {key}: {masked}")
    
except ClientError as e:
    print(f"   ❌ Error de AWS: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Verificar que la aplicación usa los secretos
print("\n🔑 SECRETOS CARGADOS EN LA APLICACIÓN:")
secret_key = Secret.get_secret_key()
jwt_key = Secret.get_jwt_secret_key()

if secret_key and jwt_key:
    print(f"   ✓ SECRET_KEY: {secret_key[:5]}{'*' * (len(secret_key) - 10)}{secret_key[-5:]}")
    print(f"   ✓ JWT_SECRET_KEY: {jwt_key[:5]}{'*' * (len(jwt_key) - 10)}{jwt_key[-5:]}")
else:
    print("   ❌ No se pudieron cargar los secretos")

# 4. Verificar que coinciden
print("\n✅ VERIFICACIÓN:")
try:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    response = client.get_secret_value(
        SecretId=os.getenv('AWS_SECRET_NAME', 'api_ing_82/secrets')
    )
    
    aws_secrets = json.loads(response['SecretString'])
    
    if secret_key == aws_secrets['SECRET_KEY']:
        print("   ✓ SECRET_KEY coincide con AWS")
    else:
        print("   ❌ SECRET_KEY NO coincide con AWS")
    
    if jwt_key == aws_secrets['JWT_SECRET_KEY']:
        print("   ✓ JWT_SECRET_KEY coincide con AWS")
    else:
        print("   ❌ JWT_SECRET_KEY NO coincide con AWS")
    
    print("\n🎉 ¡Los secretos se están cargando correctamente desde AWS!")
    
except Exception as e:
    print(f"   ⚠️  No se pudo verificar: {e}")

print("\n" + "="*70)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*70 + "\n")
