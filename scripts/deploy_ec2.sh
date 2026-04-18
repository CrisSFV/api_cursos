#!/bin/bash
# Script de despliegue en AWS EC2 (Phase 2)
# Uso: bash deploy_ec2.sh

set -e

echo "======================================"
echo "🚀 Script de Despliegue AWS EC2"
echo "======================================"

# Variables
REPO_URL="https://gitlab.com/tu-repo/api-cursos.git"
EC2_USER="ec2-user"
EC2_KEY_PATH="$HOME/.ssh/tu-key.pem"
EC2_IP="${1:?Proporciona la IP de EC2}"
APP_DIR="/app"
APP_NAME="api-cursos"

echo "📍 Desplegando en EC2: $EC2_IP"

# 1. Conectar a EC2 y clonar repositorio
echo "📥 Clonando repositorio en EC2..."
ssh -i "$EC2_KEY_PATH" "$EC2_USER@$EC2_IP" "
    cd /home/$EC2_USER
    if [ -d '$APP_DIR' ]; then
        echo '🔄 Repositorio ya existe, actualizando...'
        cd $APP_DIR
        git pull origin develop
    else
        echo '🆕 Clonando nuevo repositorio...'
        sudo mkdir -p $APP_DIR
        sudo chown $EC2_USER:$EC2_USER $APP_DIR
        git clone $REPO_URL $APP_DIR
        cd $APP_DIR
    fi
"

# 2. Instalar Docker si no existe
echo "🐳 Verificando Docker..."
ssh -i "$EC2_KEY_PATH" "$EC2_USER@$EC2_IP" "
    if ! command -v docker &> /dev/null; then
        echo '📦 Instalando Docker...'
        sudo yum update -y
        sudo yum install -y docker
        sudo systemctl start docker
        sudo usermod -aG docker $EC2_USER
        newgrp docker
    else
        echo '✅ Docker ya está instalado'
    fi
"

# 3. Construir y ejecutar imagen Docker
echo "🔨 Construyendo imagen Docker..."
ssh -i "$EC2_KEY_PATH" "$EC2_USER@$EC2_IP" "
    cd $APP_DIR
    docker build -t $APP_NAME:latest .
    
    # Detener contenedor anterior
    docker stop $APP_NAME || true
    docker rm $APP_NAME || true
    
    # Ejecutar nuevo contenedor
    docker run -d \
        --name $APP_NAME \
        --restart always \
        -p 5000:5000 \
        --env-file .env \
        $APP_NAME:latest
    
    echo '✅ Contenedor corriendo'
    docker logs -f $APP_NAME &
"

# 4. Verificar salud de la API
echo "🏥 Verificando salud de la API..."
sleep 5
if curl -f "http://$EC2_IP:5000/api/v1" > /dev/null 2>&1; then
    echo "✅ API está saludable!"
else
    echo "⚠️ API no responde. Verifica los logs en EC2."
    exit 1
fi

echo "======================================"
echo "✅ Despliegue completado exitosamente"
echo "======================================"
echo "🌐 API disponible en: http://$EC2_IP:5000"
echo "📚 Documentación en: http://$EC2_IP:5000/apidocs"
