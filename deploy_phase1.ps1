#!/usr/bin/env pwsh
<#
    Script para desplegar Fase 1: Lambda + API Gateway con stages DEV y PROD
    Requisitos: AWS CLI configurado, PowerShell 7+
#>

# Variables de configuración
$FUNCTION_NAME = "holaLambda"
$ROLE_NAME = "lambda-api-gateway-role"
$API_NAME = "holaAPI"
$REGION = "us-east-1"  # Cambiar según tu región
$ACCOUNT_ID = aws sts get-caller-identity --query Account --output text 2>$null

if (-not $ACCOUNT_ID) {
    Write-Host "Error: No se puede obtener el Account ID. Verifica tu configuración de AWS." -ForegroundColor Red
    exit 1
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "FASE 1: Lambda + API Gateway Deployment" -ForegroundColor Green
Write-Host "Account ID: $ACCOUNT_ID | Region: $REGION" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan

# Paso 1: Crear ZIP de la función Lambda
Write-Host "`n[1/6] Preparando función Lambda..." -ForegroundColor Green
$LAMBDA_DIR = "$(Get-Location)\lambda"
$ZIP_FILE = "$LAMBDA_DIR\lambda_function.zip"

if (Test-Path $ZIP_FILE) {
    Remove-Item $ZIP_FILE -Force
}

if (Test-Path $LAMBDA_DIR) {
    Compress-Archive -Path "$LAMBDA_DIR\lambda_function.py" -DestinationPath $ZIP_FILE -Force
    Write-Host "✓ ZIP creado: $ZIP_FILE" -ForegroundColor Green
} else {
    Write-Host "✗ Directorio lambda no encontrado" -ForegroundColor Red
    exit 1
}

# Paso 2: Crear rol IAM (si no existe)
Write-Host "`n[2/6] Configurando permisos IAM..." -ForegroundColor Green
$ROLE_ARN = aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>$null

if (-not $ROLE_ARN) {
    Write-Host "  Creando rol IAM: $ROLE_NAME"
    
    $TRUST_POLICY = @{
        Version = "2012-10-17"
        Statement = @(
            @{
                Effect = "Allow"
                Principal = @{
                    Service = "lambda.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        )
    } | ConvertTo-Json

    $ROLE_ARN = aws iam create-role `
        --role-name $ROLE_NAME `
        --assume-role-policy-document $TRUST_POLICY `
        --query 'Role.Arn' `
        --output text
    
    # Agregar política de logs
    aws iam attach-role-policy `
        --role-name $ROLE_NAME `
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    
    Write-Host "✓ Rol creado: $ROLE_ARN" -ForegroundColor Green
} else {
    Write-Host "✓ Rol existente: $ROLE_ARN" -ForegroundColor Green
}

# Dar tiempo para que el rol se propague
Start-Sleep -Seconds 3

# Paso 3: Crear o actualizar función Lambda
Write-Host "`n[3/6] Desplegando función Lambda..." -ForegroundColor Green

$LAMBDA_EXISTS = aws lambda get-function --function-name $FUNCTION_NAME --region $REGION 2>$null

if ($LAMBDA_EXISTS) {
    Write-Host "  Actualizando función existente..."
    aws lambda update-function-code `
        --function-name $FUNCTION_NAME `
        --zip-file fileb://$ZIP_FILE `
        --region $REGION | Out-Null
    Write-Host "✓ Función actualizada" -ForegroundColor Green
} else {
    Write-Host "  Creando nueva función..."
    aws lambda create-function `
        --function-name $FUNCTION_NAME `
        --runtime python3.11 `
        --role $ROLE_ARN `
        --handler lambda_function.lambda_handler `
        --zip-file fileb://$ZIP_FILE `
        --region $REGION | Out-Null
    Write-Host "✓ Función creada" -ForegroundColor Green
}

# Paso 4: Crear API Gateway
Write-Host "`n[4/6] Configurando API Gateway..." -ForegroundColor Green

$API_ID = aws apigateway get-rest-apis `
    --query "items[?name=='$API_NAME'].id" `
    --output text `
    --region $REGION 2>$null

if (-not $API_ID) {
    Write-Host "  Creando API REST..."
    $API_ID = aws apigateway create-rest-api `
        --name $API_NAME `
        --description "API con Stages DEV y PROD" `
        --query 'id' `
        --output text `
        --region $REGION
    Write-Host "✓ API creada: $API_ID" -ForegroundColor Green
} else {
    Write-Host "✓ API existente: $API_ID" -ForegroundColor Green
}

# Paso 5: Configurar recursos y métodos
Write-Host "`n[5/6] Configurando métodos HTTP..." -ForegroundColor Green

# Obtener recurso raíz
$ROOT_ID = aws apigateway get-resources `
    --rest-api-id $API_ID `
    --query 'items[?path=`/`].id' `
    --output text `
    --region $REGION

# Crear integración Lambda (GET)
aws apigateway put-method `
    --rest-api-id $API_ID `
    --resource-id $ROOT_ID `
    --http-method GET `
    --type AWS_PROXY `
    --authorization-type NONE `
    --region $REGION 2>$null

aws apigateway put-integration `
    --rest-api-id $API_ID `
    --resource-id $ROOT_ID `
    --http-method GET `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}/invocations" `
    --region $REGION 2>$null

# Crear integración Lambda (POST)
aws apigateway put-method `
    --rest-api-id $API_ID `
    --resource-id $ROOT_ID `
    --http-method POST `
    --type AWS_PROXY `
    --authorization-type NONE `
    --region $REGION 2>$null

aws apigateway put-integration `
    --rest-api-id $API_ID `
    --resource-id $ROOT_ID `
    --http-method POST `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}/invocations" `
    --region $REGION 2>$null

Write-Host "✓ Métodos GET y POST configurados" -ForegroundColor Green

# Paso 6: Crear stages DEV y PROD
Write-Host "`n[6/6] Creando stages DEV y PROD..." -ForegroundColor Green

# Desplegar API (crear deployment)
$DEPLOYMENT_ID = aws apigateway create-deployment `
    --rest-api-id $API_ID `
    --description "Deployment Inicial" `
    --query 'id' `
    --output text `
    --region $REGION

Write-Host "✓ Deployment creado: $DEPLOYMENT_ID" -ForegroundColor Green

# Crear stage DEV
aws apigateway create-stage `
    --rest-api-id $API_ID `
    --stage-name dev `
    --deployment-id $DEPLOYMENT_ID `
    --description "Desarrollo" `
    --region $REGION 2>$null

# Crear stage PROD
aws apigateway create-stage `
    --rest-api-id $API_ID `
    --stage-name prod `
    --deployment-id $DEPLOYMENT_ID `
    --description "Producción" `
    --region $REGION 2>$null

Write-Host "✓ Stages creados: dev y prod" -ForegroundColor Green

# Otorgar permisos a API Gateway para invocar Lambda
Write-Host "`nConfigurando permisos Lambda..." -ForegroundColor Green

aws lambda add-permission `
    --function-name $FUNCTION_NAME `
    --statement-id AllowAPIGateway `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${API_ID}/*/*" `
    --region $REGION 2>$null

Write-Host "✓ Permisos otorgados" -ForegroundColor Green

# Resumen Final
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "✓ FASE 1 COMPLETADA" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`n📋 URLS DE PRUEBA:" -ForegroundColor Yellow
Write-Host "DEV:  https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev" -ForegroundColor Cyan
Write-Host "PROD: https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod" -ForegroundColor Cyan

Write-Host "`n🔧 COMANDOS CURL PARA PRUEBAS:" -ForegroundColor Yellow
Write-Host "GET DEV:  curl -X GET https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev" -ForegroundColor White
Write-Host "POST DEV: curl -X POST https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev -H 'Content-Type: application/json'" -ForegroundColor White
Write-Host "GET PROD:  curl -X GET https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod" -ForegroundColor White
Write-Host "POST PROD: curl -X POST https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod -H 'Content-Type: application/json'" -ForegroundColor White

Write-Host "`n📦 INFORMACIÓN GUARDADA:" -ForegroundColor Yellow
Write-Host "Lambda Function: $FUNCTION_NAME" -ForegroundColor White
Write-Host "API Gateway ID: $API_ID" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White

# Guardar información en archivo
$INFO = @"
# Fase 1 Deployment Info
API_ID=$API_ID
FUNCTION_NAME=$FUNCTION_NAME
REGION=$REGION
ACCOUNT_ID=$ACCOUNT_ID
DEPLOYMENT_DATE=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# DEV URLs
DEV_GET=https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev
DEV_POST=https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev

# PROD URLs
PROD_GET=https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod
PROD_POST=https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod
"@

$INFO | Out-File -FilePath "$(Get-Location)\phase1_info.env" -Encoding UTF8 -Force
Write-Host "`n✓ Información guardada en: phase1_info.env" -ForegroundColor Green

Write-Host "`n================================================`n" -ForegroundColor Cyan
