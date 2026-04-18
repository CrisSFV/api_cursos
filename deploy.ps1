param(
    [string]$REGION = "us-east-1"
)

$FUNCTION_NAME = "holaLambda"
$ROLE_NAME = "lambda-api-gateway-role"
$API_NAME = "holaAPI"
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text 2>$null)

if (-not $ACCOUNT_ID) {
    Write-Host "Error: Verifica configuracion AWS CLI" -ForegroundColor Red
    exit 1
}

Write-Host "`nIniciando Fase 1: Lambda + API Gateway`n" -ForegroundColor Green
Write-Host "Region: $REGION | Account: $ACCOUNT_ID`n" -ForegroundColor Yellow

# 1. Crear ZIP
Write-Host "[1/5] Preparando ZIP..." -ForegroundColor Green
$ZIP = "lambda\lambda_function.zip"
if (Test-Path $ZIP) { Remove-Item $ZIP -Force }
Compress-Archive -Path "lambda\lambda_function.py" -DestinationPath $ZIP -Force
Write-Host "OK: ZIP creado`n"

# 2. Crear rol IAM
Write-Host "[2/5] Configurando IAM..." -ForegroundColor Green
$ROLE = aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>$null
if (-not $ROLE) {
    $TRUST = '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}'
    $ROLE = (aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document $TRUST --query 'Role.Arn' --output text)
    aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Start-Sleep -Seconds 2
}
Write-Host "OK: IAM configurado ($ROLE)`n"

# 3. Crear/Actualizar Lambda
Write-Host "[3/5] Deploying Lambda..." -ForegroundColor Green
$FUNC = aws lambda get-function --function-name $FUNCTION_NAME --region $REGION 2>$null
if ($FUNC) {
    aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP --region $REGION | Out-Null
    Write-Host "OK: Funcion actualizada`n"
} else {
    aws lambda create-function --function-name $FUNCTION_NAME --runtime python3.11 --role $ROLE --handler lambda_function.lambda_handler --zip-file fileb://$ZIP --region $REGION | Out-Null
    Write-Host "OK: Funcion creada`n"
}

# 4. Crear/Configurar API Gateway
Write-Host "[4/5] Configurando API Gateway..." -ForegroundColor Green
$API_ID = (aws apigateway get-rest-apis --query "items[?name=='$API_NAME'].id" --output text --region $REGION 2>$null)
if (-not $API_ID) {
    $API_ID = (aws apigateway create-rest-api --name $API_NAME --description "API DEV/PROD" --query 'id' --output text --region $REGION)
    Write-Host "OK: API creada ($API_ID)"
} else {
    Write-Host "OK: API existente ($API_ID)"
}

$ROOT_ID = (aws apigateway get-resources --rest-api-id $API_ID --query 'items[?path==`/`].id' --output text --region $REGION)

# Crear metodos GET y POST
aws apigateway put-method --rest-api-id $API_ID --resource-id $ROOT_ID --http-method GET --type AWS_PROXY --authorization-type NONE --region $REGION 2>$null
aws apigateway put-integration --rest-api-id $API_ID --resource-id $ROOT_ID --http-method GET --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}/invocations" --region $REGION 2>$null

aws apigateway put-method --rest-api-id $API_ID --resource-id $ROOT_ID --http-method POST --type AWS_PROXY --authorization-type NONE --region $REGION 2>$null
aws apigateway put-integration --rest-api-id $API_ID --resource-id $ROOT_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}/invocations" --region $REGION 2>$null

Write-Host "OK: Metodos HTTP configurados`n"

# 5. Crear Stages
Write-Host "[5/5] Creando Stages DEV y PROD..." -ForegroundColor Green
$DEPLOY = (aws apigateway create-deployment --rest-api-id $API_ID --description "Inicial" --query 'id' --output text --region $REGION)
aws apigateway create-stage --rest-api-id $API_ID --stage-name dev --deployment-id $DEPLOY --description "Desarrollo" --region $REGION 2>$null
aws apigateway create-stage --rest-api-id $API_ID --stage-name prod --deployment-id $DEPLOY --description "Produccion" --region $REGION 2>$null

# Permisos Lambda
aws lambda add-permission --function-name $FUNCTION_NAME --statement-id AllowAPIGateway --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${API_ID}/*/*" --region $REGION 2>$null

Write-Host "OK: Stages creados`n"

# Resumen
Write-Host "=== FASE 1 COMPLETADA ===" -ForegroundColor Green
Write-Host "`nURLs de Prueba:" -ForegroundColor Cyan
Write-Host "  DEV:  https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev" -ForegroundColor White
Write-Host "  PROD: https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod`n" -ForegroundColor White

Write-Host "Comandos CURL:" -ForegroundColor Cyan
Write-Host "  curl -X GET https://${API_ID}.execute-api.${REGION}.amazonaws.com/dev" -ForegroundColor White
Write-Host "  curl -X GET https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod`n" -ForegroundColor White

# Guardar info
@"
API_ID=$API_ID
FUNCTION_NAME=$FUNCTION_NAME
REGION=$REGION
ACCOUNT_ID=$ACCOUNT_ID
DEPLOYMENT_DATE=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@ | Out-File phase1_info.env -Force
Write-Host "Informacion guardada en: phase1_info.env`n"
