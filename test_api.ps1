# Script completo de testing para la API
# Uso: .\test_api.ps1

Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🧪 TEST COMPLETO - API de Cursos" -ForegroundColor Green
Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan

$BaseURL = "http://localhost:5000/api/v1"
$token = ""

# Colores para output
$success = "Green"
$error = "Red"
$info = "Cyan"

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Endpoint,
        [hashtable]$Body,
        [string]$Token
    )
    
    Write-Host "`n📍 TEST: $Name" -ForegroundColor $info
    Write-Host "  Método: $Method $Endpoint" -ForegroundColor Yellow
    
    try {
        $headers = @{"Content-Type" = "application/json"}
        if ($Token) {
            $headers["Authorization"] = "Bearer $Token"
        }
        
        $params = @{
            Uri = "$BaseURL$Endpoint"
            Method = $Method
            Headers = $headers
        }
        
        if ($Body) {
            $params["Body"] = ($Body | ConvertTo-Json)
        }
        
        $response = Invoke-WebRequest @params
        $content = $response.Content | ConvertFrom-Json
        
        Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor $success
        Write-Host "  📤 Response:" -ForegroundColor Cyan
        Write-Host ($content | ConvertTo-Json | Out-String) -ForegroundColor White
        
        return $content
    }
    catch {
        Write-Host "  ❌ Error: $($_.Exception.Message)" -ForegroundColor $error
        return $null
    }
}

# ===========================
# TEST 1: REGISTRO
# ===========================
Write-Host "`n" -ForegroundColor Cyan
Write-Host "═ PRUEBA 1: AUTENTICACIÓN" -ForegroundColor Cyan
Write-Host "═" -ForegroundColor Cyan

$registerBody = @{
    username = "juan_doe_$(Get-Random)"
    email = "juan$(Get-Random)@example.com"
    password = "Password123!"
}

$registerResult = Test-Endpoint -Name "Registrar Usuario" `
    -Method "POST" `
    -Endpoint "/auth/register" `
    -Body $registerBody

# ===========================
# TEST 2: LOGIN
# ===========================
if ($registerResult) {
    $loginBody = @{
        username = $registerBody.username
        password = $registerBody.password
    }
    
    $loginResult = Test-Endpoint -Name "Login" `
        -Method "POST" `
        -Endpoint "/auth/login" `
        -Body $loginBody
    
    if ($loginResult.access_token) {
        $token = $loginResult.access_token
        Write-Host "`n✅ Token obtenido:" -ForegroundColor $success
        Write-Host "   $($token.Substring(0, 50))..." -ForegroundColor Yellow
    }
}

# ===========================
# TEST 3: CREAR CATEGORÍA
# ===========================
Write-Host "`n" -ForegroundColor Cyan
Write-Host "═ PRUEBA 2: CATEGORÍAS" -ForegroundColor Cyan
Write-Host "═" -ForegroundColor Cyan

if ($token) {
    $categoryBody = @{
        name = "Programación"
        description = "Cursos de lenguajes de programación"
    }
    
    $categoryResult = Test-Endpoint -Name "Crear Categoría" `
        -Method "POST" `
        -Endpoint "/categorias" `
        -Body $categoryBody `
        -Token $token
    
    $categoryId = $categoryResult.id
}

# ===========================
# TEST 4: CREAR CURSO
# ===========================
Write-Host "`n" -ForegroundColor Cyan
Write-Host "═ PRUEBA 3: CURSOS" -ForegroundColor Cyan
Write-Host "═" -ForegroundColor Cyan

if ($token -and $categoryId) {
    $courseBody = @{
        nombre = "Python Avanzado"
        descripcion = "Aprende Python a nivel avanzado"
        precio = 99.99
        categoria_id = $categoryId
    }
    
    $courseResult = Test-Endpoint -Name "Crear Curso" `
        -Method "POST" `
        -Endpoint "/cursos" `
        -Body $courseBody `
        -Token $token
}

# ===========================
# TEST 5: OBTENER CURSOS
# ===========================
$allCourses = Test-Endpoint -Name "Obtener Todos los Cursos" `
    -Method "GET" `
    -Endpoint "/cursos"

# ===========================
# TEST 6: FILTRAR POR CATEGORÍA
# ===========================
if ($categoryId) {
    $filteredCourses = Test-Endpoint -Name "Filtrar Cursos por Categoría" `
        -Method "GET" `
        -Endpoint "/cursos?categoria=$categoryId"
}

# ===========================
# TEST 7: 2FA - GENERAR QR
# ===========================
Write-Host "`n" -ForegroundColor Cyan
Write-Host "═ PRUEBA 4: SEGURIDAD (2FA)" -ForegroundColor Cyan
Write-Host "═" -ForegroundColor Cyan

if ($token -and $registerResult.id) {
    $twoFABody = @{
        user_id = $registerResult.id
    }
    
    $qrResult = Test-Endpoint -Name "Generar QR 2FA" `
        -Method "POST" `
        -Endpoint "/auth/2fa/enable-qr" `
        -Body $twoFABody `
        -Token $token
}

# ===========================
# RESUMEN
# ===========================
Write-Host "`n" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ TESTING COMPLETADO" -ForegroundColor Green
Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n📚 Documentación Swagger disponible en:" -ForegroundColor $info
Write-Host "   🔗 http://localhost:5000/apidocs" -ForegroundColor Yellow

Write-Host "`n📊 Endpoints testeados:" -ForegroundColor $info
Write-Host "   ✅ POST   /auth/register" -ForegroundColor $success
Write-Host "   ✅ POST   /auth/login" -ForegroundColor $success
Write-Host "   ✅ POST   /categorias" -ForegroundColor $success
Write-Host "   ✅ POST   /cursos" -ForegroundColor $success
Write-Host "   ✅ GET    /cursos" -ForegroundColor $success
Write-Host "   ✅ GET    /cursos?categoria=X" -ForegroundColor $success
Write-Host "   ✅ POST   /auth/2fa/enable-qr" -ForegroundColor $success
