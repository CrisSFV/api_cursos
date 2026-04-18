param(
    [string]$REGION = "us-east-1"
)

$FunctionName = "holaLambda"
$RoleName = "lambda-api-gateway-role"
$ApiName = "holaAPI"
$AccountId = (aws sts get-caller-identity --query Account --output text)

Write-Host "`nPhase 1: Lambda + API Gateway with Dev/Prod Stages`n" -ForegroundColor Green
Write-Host "Region: $REGION | Account: $AccountId`n" -ForegroundColor Yellow

# Step 1: Create ZIP
Write-Host "[1/5] Creating ZIP..." -ForegroundColor Cyan
$ZipFile = "lambda_function.zip"
if (Test-Path $ZipFile) { Remove-Item $ZipFile -Force }

if (Test-Path "lambda") {
    Compress-Archive -Path "lambda\*" -DestinationPath $ZipFile -Force -ErrorAction Stop
    Write-Host "OK: ZIP created`n"
} else {
    Write-Host "ERROR: lambda folder not found`n" -ForegroundColor Red
    exit 1
}

# Step 2: Create IAM Role
Write-Host "[2/5] Setting up IAM..." -ForegroundColor Cyan
$RoleArn = (aws iam get-role --role-name $RoleName --query 'Role.Arn' --output text 2>&1)

if ($RoleArn -like "*NoSuchEntity*" -or -not $RoleArn) {
    Write-Host "Creating IAM role..."
    $RoleArn = (aws iam create-role `
        --role-name $RoleName `
        --assume-role-policy-document file://trust-policy.json `
        --query 'Role.Arn' `
        --output text)
    
    Write-Host "Attaching execution policy..."
    aws iam attach-role-policy `
        --role-name $RoleName `
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    
    Start-Sleep -Seconds 3
}

Write-Host "OK: Role ARN = $RoleArn`n"

# Step 3: Create/Update Lambda
Write-Host "[3/5] Deploying Lambda function..." -ForegroundColor Cyan

$LambdaExists = (aws lambda get-function --function-name $FunctionName --region $REGION 2>&1)

if ($LambdaExists -like "*FunctionNotFound*") {
    Write-Host "Creating function..."
    aws lambda create-function `
        --function-name $FunctionName `
        --runtime python3.11 `
        --role $RoleArn `
        --handler lambda_function.lambda_handler `
        --zip-file fileb://$ZipFile `
        --region $REGION
    Write-Host "OK: Function created"
} else {
    Write-Host "Updating function..."
    aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file fileb://$ZipFile `
        --region $REGION | Out-Null
    Write-Host "OK: Function updated"
}
Write-Host ""

# Step 4: Create/Config API Gateway
Write-Host "[4/5] Configuring API Gateway..." -ForegroundColor Cyan

$ApiId = (aws apigateway get-rest-apis --query "items[?name=='$ApiName'].id" --output text --region $REGION 2>&1)

if (-not $ApiId -or $ApiId -like "*None*") {
    Write-Host "Creating REST API..."
    $ApiId = (aws apigateway create-rest-api `
        --name $ApiName `
        --description "API with DEV/PROD stages" `
        --query 'id' `
        --output text `
        --region $REGION)
    Write-Host "OK: API created - $ApiId"
} else {
    Write-Host "OK: API exists - $ApiId"
}

$RootId = (aws apigateway get-resources `
    --rest-api-id $ApiId `
    --query 'items[?path==`/`].id' `
    --output text `
    --region $REGION)

Write-Host "Root resource: $RootId"

# Create GET method
Write-Host "Creating GET method..."
aws apigateway put-method `
    --rest-api-id $ApiId `
    --resource-id $RootId `
    --http-method GET `
    --type AWS_PROXY `
    --authorization-type NONE `
    --region $REGION 2>&1 | out-Null

aws apigateway put-integration `
    --rest-api-id $ApiId `
    --resource-id $RootId `
    --http-method GET `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${AccountId}:function:${FunctionName}/invocations" `
    --region $REGION 2>&1 | out-Null

# Create POST method
Write-Host "Creating POST method..."
aws apigateway put-method `
    --rest-api-id $ApiId `
    --resource-id $RootId `
    --http-method POST `
    --type AWS_PROXY `
    --authorization-type NONE `
    --region $REGION 2>&1 | out-Null

aws apigateway put-integration `
    --rest-api-id $ApiId `
    --resource-id $RootId `
    --http-method POST `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:${REGION}:${AccountId}:function:${FunctionName}/invocations" `
    --region $REGION 2>&1 | out-Null

Write-Host "OK: Methods configured`n"

# Step 5: Create Deployment & Stages
Write-Host "[5/5] Creating Stages..." -ForegroundColor Cyan

$DeployId = (aws apigateway create-deployment `
    --rest-api-id $ApiId `
    --description "Initial deployment" `
    --query 'id' `
    --output text `
    --region $REGION)

Write-Host "Deployment: $DeployId"

aws apigateway create-stage `
    --rest-api-id $ApiId `
    --stage-name dev `
    --deployment-id $DeployId `
    --description "Development" `
    --region $REGION 2>&1 | out-Null

aws apigateway create-stage `
    --rest-api-id $ApiId `
    --stage-name prod `
    --deployment-id $DeployId `
    --description "Production" `
    --region $REGION 2>&1 | out-Null

Write-Host "OK: Stages created (dev, prod)"

# Grant Lambda invoke permission
Write-Host "Setting Lambda permissions..."
aws lambda add-permission `
    --function-name $FunctionName `
    --statement-id AllowAPIGtw `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:${REGION}:${AccountId}:${ApiId}/*/*" `
    --region $REGION 2>&1 | out-Null

Write-Host "OK: Permissions set`n"

# Summary
Write-Host "======================================" -ForegroundColor Green
Write-Host "PHASE 1 COMPLETED" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Green

Write-Host "Test URLs:" -ForegroundColor Cyan
Write-Host "  DEV:  https://${ApiId}.execute-api.${REGION}.amazonaws.com/dev" 
Write-Host "  PROD: https://${ApiId}.execute-api.${REGION}.amazonaws.com/prod`n"

Write-Host "CURL Commands:" -ForegroundColor Cyan
Write-Host "  curl -X GET https://${ApiId}.execute-api.${REGION}.amazonaws.com/dev"
Write-Host "  curl -X GET https://${ApiId}.execute-api.${REGION}.amazonaws.com/prod`n"

# Save config
@"
API_ID=$ApiId
FUNCTION_NAME=$FunctionName
REGION=$REGION
ACCOUNT_ID=$AccountId
ROLE_ARN=$RoleArn
DEPLOYMENT_DATE=$(Get-Date)
DEV_URL=https://${ApiId}.execute-api.${REGION}.amazonaws.com/dev
PROD_URL=https://${ApiId}.execute-api.${REGION}.amazonaws.com/prod
"@ | Out-File phase1.env -Encoding UTF8 -Force

Write-Host "Config saved to: phase1.env`n"
