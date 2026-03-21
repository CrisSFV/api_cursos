import os
import json
import boto3
from botocore.exceptions import ClientError

class Secret:
    SECRET_KEY = None
    JWT_SECRET_KEY = None
    _secrets_loaded = False

    @staticmethod
    def _load_secrets_from_aws():
        """Carga secretos desde AWS Secrets Manager"""
        secret_name = os.getenv('AWS_SECRET_NAME', 'api_ing_82/secrets')
        region_name = os.getenv('AWS_REGION', 'us-east-1')

        try:
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )
            
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            
            secret = json.loads(get_secret_value_response['SecretString'])
            Secret.SECRET_KEY = secret.get('SECRET_KEY')
            Secret.JWT_SECRET_KEY = secret.get('JWT_SECRET_KEY')
            Secret._secrets_loaded = True
            print(" Secretos cargados desde AWS Secrets Manager")
            
        except ClientError as e:
            print(f" Error al obtener secretos de AWS: {e}")
            print("  Usando valores locales para desarrollo")
            # Fallback a valores locales para desarrollo
            Secret.SECRET_KEY = 'super-secret-key-local'
            Secret.JWT_SECRET_KEY = 'jwt-super-secret-local'
            Secret._secrets_loaded = True
        except Exception as e:
            print(f" Error inesperado: {e}")
            Secret.SECRET_KEY = 'super-secret-key-local'
            Secret.JWT_SECRET_KEY = 'jwt-super-secret-local'
            Secret._secrets_loaded = True

    @staticmethod
    def get_secret_key():
        if not Secret._secrets_loaded:
            Secret._load_secrets_from_aws()
        return Secret.SECRET_KEY

    @staticmethod
    def get_jwt_secret_key():
        if not Secret._secrets_loaded:
            Secret._load_secrets_from_aws()
        return Secret.JWT_SECRET_KEY

    @staticmethod
    def set_secret_key(key):
        Secret.SECRET_KEY = key
