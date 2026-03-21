import json
import boto3
from botocore.exceptions import ClientError

class  Aws_SecretManager:
    def __init__(self):
        print('iniciando')
        self.client = boto3.client('secretsmanager')
        self.nombre = "Crispy"

def get_secret(self, secret_name):
    try:
        response = self.client.get_secret_value(
            SecretId=secret_name
        )
        secret_string = response['SecretString']
        return json.loads(secret_string)
    except ClientError as e:
        raise Exception(f"Error al obtener el secreto: {str(e)}")