import json

def lambda_handler(event, context):
    """
    Función Lambda para API Gateway con múltiples stages (dev y prod)
    Retorna mensajes diferentes según el stage invocado
    """
    
    # Obtener el stage desde el contexto de API Gateway
    stage = event.get("requestContext", {}).get("stage", "unknown")
    
    # Determinar el mensaje según el stage
    if stage == "dev":
        message = "Hola desde dev"
    elif stage == "prod":
        message = "Hola desde prod"
    else:
        message = f"Stage no reconocido: {stage}"
    
    # Construir la respuesta
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({
            "mensaje": message,
            "stage": stage
        })
    }
