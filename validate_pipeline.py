#!/usr/bin/env python
"""
Script para validar que el pipeline CI/CD funcionaría correctamente
Simula los stages del .gitlab-ci.yml localmente
"""

import os
import subprocess
import sys
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_stage(stage_name, icon="🔵"):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{icon} STAGE: {stage_name}{Colors.ENDC}")
    print("=" * 70)

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")
    return False

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def run_command(cmd, description=""):
    """Ejecutar comando y mostrar resultado"""
    if description:
        print(f"\n📝 {description}")
        print(f"   Comando: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print_success(f"Comando ejecutado correctamente")
            if result.stdout:
                print(f"   {result.stdout[:200]}")
            return True
        else:
            print_error(f"Comando falló")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Comando tardó demasiado (timeout)")
        return False
    except Exception as e:
        print_error(f"Error ejecutando comando: {str(e)}")
        return False

# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
    print("🔄 VALIDACIÓN LOCAL DEL PIPELINE CI/CD")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    all_passed = True
    
    # ===========================
    # STAGE 1: TEST
    # ===========================
    print_stage("TEST", "🔵")
    print("Objetivo: Verificar que el código sea válido\n")
    
    # Verificar syntax Python
    if run_command(
        "python -m py_compile app.py",
        "1. Verificar sintaxis del archivo principal (app.py)"
    ):
        print_success("app.py tiene sintaxis válida")
    else:
        all_passed = False
        print_error("Hay errores de sintaxis en app.py")
    
    # Verificar imports
    import_cmd = '''python -c "import flask; import flask_sqlalchemy; import flask_jwt_extended; import flasgger"'''
    if run_command(
        import_cmd,
        "2. Verificar que todas las dependencias estén instaladas"
    ):
        print_success("Todas las dependencias están instaladas")
    else:
        all_passed = False
        print_warning("Faltan dependencias (continuando...)")
    
    # Verificar structure
    print("\n📝 3. Verificar estructura del proyecto")
    required_dirs = ['controllers', 'models', 'repositories', 'services', 'migrations']
    all_dirs_ok = True
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print_success(f"Directorio '{dir_name}' existe")
        else:
            print_error(f"Falta directorio '{dir_name}'")
            all_dirs_ok = False
    
    if not all_dirs_ok:
        all_passed = False
    
    # ===========================
    # STAGE 2: BUILD
    # ===========================
    print_stage("BUILD", "🟢")
    print("Objetivo: Construir imagen Docker\n")
    
    # Verificar Dockerfile
    print("📝 1. Verificar que existe Dockerfile")
    if os.path.isfile("Dockerfile"):
        print_success("Dockerfile existe")
        
        # Validar contenido
        with open("Dockerfile", "r") as f:
            content = f.read()
            if "FROM python" in content and "EXPOSE 5000" in content:
                print_success("Dockerfile tiene estructura válida")
            else:
                print_warning("Dockerfile podría tener problemas")
    else:
        print_error("No existe Dockerfile")
        all_passed = False
    
    # Verificar requirements.txt
    print("\n📝 2. Verificar requirements.txt")
    if os.path.isfile("requirements.txt"):
        print_success("requirements.txt existe")
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            if "flask" in requirements.lower() and "sqlalchemy" in requirements.lower():
                print_success("requirements.txt tiene dependencias necesarias")
            else:
                print_warning("Faltan dependencias importantes en requirements.txt")
    else:
        print_error("No existe requirements.txt")
        all_passed = False
    
    # Verificar que Docker está instalado
    print("\n📝 3. Verificar que Docker está instalado")
    if run_command("docker --version", "Verificar instalación de Docker"):
        print_success("Docker está disponible")
    else:
        print_warning("Docker no está instalado localmente (GitLab Runners lo instalarán automáticamente)")
    
    # ===========================
    # STAGE 3: DEPLOY_DEV
    # ===========================
    print_stage("DEPLOY_DEV", "🟡")
    print("Objetivo: Desplegar a ambiente de desarrollo\n")
    
    # Verificar script de despliegue
    print("📝 1. Verificar scripts de despliegue")
    if os.path.isfile("scripts/deploy_ec2.sh"):
        print_success("scripts/deploy_ec2.sh existe")
    else:
        print_warning("Falta scripts/deploy_ec2.sh")
    
    if os.path.isfile("scripts/deploy_ec2.ps1"):
        print_success("scripts/deploy_ec2.ps1 existe")
    else:
        print_warning("Falta scripts/deploy_ec2.ps1")
    
    # Verificar variables de entorno
    print("\n📝 2. Verificar configuración de variables de entorno")
    if os.path.isfile(".env"):
        print_success(".env existe")
        with open(".env", "r") as f:
            env_content = f.read()
            if "DATABASE_URI" in env_content:
                print_success("DATABASE_URI configurado")
            else:
                print_error("DATABASE_URI no configurado")
                all_passed = False
    else:
        print_warning(".env no existe. Usa .env.example")
    
    # ===========================
    # VERIFICACIÓN FINAL
    # ===========================
    print_stage("VERIFICACIÓN FINAL", "📊")
    
    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ TODAS LAS VALIDACIONES PASARON{Colors.ENDC}")
        print("\n✅ El pipeline debería funcionar correctamente en GitLab")
        print("\nPróximos pasos:")
        print("1. Push a GitLab:")
        print("   git push -u origin develop")
        print("\n2. Monitorea el pipeline en:")
        print("   https://gitlab.com/tu-usuario/api-cursos/-/pipelines")
        print("\n3. Los stages deberían ejecutarse automáticamente")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ALGUNAS VALIDACIONES FALLARON{Colors.ENDC}")
        print("\n⚠️  Revisa los errores arriba antes de hacer push")
    
    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    sys.exit(0 if all_passed else 1)
