#!/usr/bin/env pwsh
# Phase 1: Complete AWS Lambda + API Gateway Setup

param([string]$Region = "us-east-1")

$FuncName = "holaLambda"
$RoleName = "lambda-api-gateway-role"
$ApiName = "holaAPI"
$AccountId = (aws sts get-caller-identity --query Account --output text)

function Log([string]$msg, [string]$color = "Green") {
    Write-Host $msg -ForegroundColor $color
}

Log "`n=== AWS Phase 1 Deployment ===" "Cyan"
Log "Account: $AccountId | Region: $Region`n"

# Step 1: ZIP
Log "[1] Creating Lambda package..."
if (Test-Path "lambda_function.zip") {
    Remove-Item "lambda_function.zip" -Force
}
Compress-Archive -Path "lambda\lambda_function.py" -DestinationPath "lambda_function.zip" -Force
Log "Done: lambda_function.zip`n" "Yellow"

# Step 2: Role
Log "[2] Setting up IAM Role..."
$roleCheck = aws iam get-role --role-name $RoleName 2>&1
if ($LASTEXITCODE -ne 0) {
    Log "Creating new role..." "Yellow"
    aws iam create-role --role-name $RoleName --assume-role-policy-document file://trust-policy.json
    aws iam attach-role-policy --role-name $RoleName --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Start-Sleep -Seconds 3
    Log "Role created" "Yellow"
} else {
    Log "Role exists" "Yellow"
}

$RoleArn = aws iam get-role --role-name $RoleName --query 'Role.Arn' --output text
Log "Role ARN: $RoleArn`n"

# Step 3: Lambda
Log "[3] Creating Lambda Function..."
$funcCheck = aws lambda get-function --function-name $FuncName --region $Region 2>&1

if ($LASTEXITCODE -ne 0) {
    Log "Creating function..." "Yellow"
    aws lambda create-function `
        --function-name $FuncName `
        --runtime python3.11 `
        --role $RoleArn `
        --handler lambda_function.lambda_handler `
        --zip-file fileb://lambda_function.zip `
        --region $Region --timeout 10 --memory-size 128
    Log "Function created" "Yellow"
} else {
    Log "Updating function..." "Yellow"  
    aws lambda update-function-code `
        --function-name $FuncName `
        --zip-file fileb://lambda_function.zip `
        --region $Region
}
Log "Done`n" "Yellow"

# Step 4: API Gateway
Log "[4] Setting up API Gateway..."
$apiCheck = aws apigateway get-rest-apis --query "items[?name=='$ApiName'].id" --output text --region $Region 2>&1

if ([string]::IsNullOrEmpty($apiCheck)) {
    Log "Creating API..." "Yellow"
    $ApiId = aws apigateway create-rest-api --name $ApiName --description "Lambda DEV/PROD" --query 'id' --output text --region $Region
} else {
    $ApiId = $apiCheck
    Log "API exists" "Yellow"
}

Log "API ID: $ApiId`n" "Yellow"

# Get root resource
$RootId = aws apigateway get-resources --rest-api-id $ApiId --query 'items[?path==`/`].id' --output text --region $Region

Log "Root ID: $RootId"
Log "Configuring methods..." "Yellow"

# PUT method + integration (GET)
aws apigateway put-method --rest-api-id $ApiId --resource-id $RootId --http-method GET --type AWS_PROXY --authorization-type NONE --region $Region --no-cli-pager

$integUri = "arn:aws:apigateway:${Region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${Region}:${AccountId}:function:${FuncName}/invocations"

aws apigateway put-integration --rest-api-id $ApiId --resource-id $RootId --http-method GET --type AWS_PROXY --integration-http-method POST --uri $integUri --region $Region --no-cli-pager

# PUT method + integration (POST)
aws apigateway put-method --rest-api-id $ApiId --resource-id $RootId --http-method POST --type AWS_PROXY --authorization-type NONE --region $Region --no-cli-pager

aws apigateway put-integration --rest-api-id $ApiId --resource-id $RootId --http-method POST --type AWS_PROXY --integration-http-method POST --uri $integUri --region $Region --no-cli-pager

Log "Methods configured`n" "Yellow"

# Verify methods exist
Log "Verifying methods..." "Yellow"
$methods = aws apigateway get-resource --rest-api-id $ApiId --resource-id $RootId --region $Region --query 'resourceMethods' --output text
Log "Methods: $methods`n"

# Step 5: Deployment
Log "[5] Creating Deployment & Stages..."

$DeployId = aws apigateway create-deployment --rest-api-id $ApiId --description "Initial" --region $Region --query 'id' --output text

Log "Deployment: $DeployId"

aws apigateway create-stage --rest-api-id $ApiId --stage-name dev --deployment-id $DeployId --description "Development" --region $Region
aws apigateway create-stage --rest-api-id $ApiId --stage-name prod --deployment-id $DeployId --description "Production" --region $Region

Log "Stages: dev, prod`n" "Yellow"

# Lambda Permissions
Log "Setting Lambda permissions..." "Yellow"
$SourceArn = "arn:aws:execute-api:${Region}:${AccountId}:${ApiId}/*/*"
aws lambda add-permission --function-name $FuncName --statement-id AllowAPIGateway --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn $SourceArn --region $Region 2>&1

Log "Done`n" "Yellow"

# Output
Log "=== DEPLOYMENT COMPLETE ===" "Green"
Log "`nEndpoints:" "Cyan"
Log "  DEV:  https://${ApiId}.execute-api.${Region}.amazonaws.com/dev"
Log "  PROD: https://${ApiId}.execute-api.${Region}.amazonaws.com/prod"

Log "`nTest with curl:" "Cyan"
Log "  curl https://${ApiId}.execute-api.${Region}.amazonaws.com/dev"
Log "  curl https://${ApiId}.execute-api.${Region}.amazonaws.com/prod`n"

# Save env
$env_content = @"
API_ID=$ApiId
FUNCTION_NAME=$FuncName
REGION=$Region
ACCOUNT_ID=$AccountId
ROLE_ARN=$RoleArn
DEV_ENDPOINT=https://${ApiId}.execute-api.${Region}.amazonaws.com/dev
PROD_ENDPOINT=https://${ApiId}.execute-api.${Region}.amazonaws.com/prod
DATETIME=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

$env_content | Out-File phase1.env -Encoding UTF8 -Force
Log "Config saved: phase1.env`n" "Yellow"
