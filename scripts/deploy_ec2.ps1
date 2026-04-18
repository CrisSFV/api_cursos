# Script de Despliegue AWS EC2 - Windows PowerShell
# Uso: .\deploy_ec2.ps1 -EC2IP "54.123.45.67" -KeyPath "C:\path\to\key.pem"

param(
    [Parameter(Mandatory=$true)]
    [string]$EC2IP,
    
    [Parameter(Mandatory=$true)]
    [string]$KeyPath,
    
    [string]$EC2User = "ec2-user",
    [string]$AppDir = "/app",
    [string]$AppName = "api-cursos"
)

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🚀 Script de Despliegue AWS EC2 (PowerShell)" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

# Verificar que PuTTY/SSH esté disponible
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ SSH no está instalado. Instala Git for Windows o WSL." -ForegroundColor Red
    exit 1
}

# 1. Clonar repositorio
Write-Host "📥 Actualizando repositorio en EC2..." -ForegroundColor Yellow
$sshCmd = @"
    cd /home/$EC2User
    if [ -d '$AppDir' ]; then
        cd $AppDir
        git pull origin develop
    else
        git clone https://gitlab.com/tu-repo/api-cursos.git $AppDir
        cd $AppDir
    fi
"@

ssh -i "$KeyPath" "$EC2User@$EC2IP" $sshCmd

# 2. Construir imagen Docker
Write-Host "🐳 Construyendo imagen Docker..." -ForegroundColor Yellow
$dockerCmd = @"
    cd $AppDir
    docker build -t $AppName:latest .
    docker stop $AppName || true
    docker rm $AppName || true
    docker run -d \
        --name $AppName \
        --restart always \
        -p 5000:5000 \
        --env-file .env \
        $AppName:latest
    sleep 5
    docker logs $AppName
"@

ssh -i "$KeyPath" "$EC2User@$EC2IP" $dockerCmd

# 3. Verificar salud
Write-Host "🏥 Verificando salud de la API..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://$EC2IP:5000/api/v1" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API está saludable!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ API no responde. Verifica los logs en EC2." -ForegroundColor Yellow
    exit 1
}

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ Despliegue completado exitosamente" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🌐 API disponible en: http://$EC2IP:5000" -ForegroundColor Cyan
Write-Host "📚 Documentación en: http://$EC2IP:5000/apidocs" -ForegroundColor Cyan
