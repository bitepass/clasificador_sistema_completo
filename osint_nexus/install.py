#!/usr/bin/env python3
"""
Script de instalación para OSINT-Nexus
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """Muestra el banner de instalación"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          🔍 OSINT-NEXUS INSTALLER 🔍                        ║
║                                                                              ║
║                     Plataforma de Inteligencia Automatizada                 ║
║                                Version 1.0.0                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detectado")

def check_system():
    """Verifica el sistema operativo"""
    print("💻 Verificando sistema operativo...")
    
    os_name = platform.system()
    print(f"✅ Sistema operativo: {os_name}")
    
    if os_name == "Windows":
        print("ℹ️  Detectado Windows - Asegúrese de tener Git Bash o WSL instalado")
    elif os_name == "Darwin":
        print("ℹ️  Detectado macOS")
    elif os_name == "Linux":
        print("ℹ️  Detectado Linux")
    else:
        print("⚠️  Sistema operativo no reconocido, continuando...")

def install_requirements():
    """Instala las dependencias de Python"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def create_directories():
    """Crea directorios necesarios"""
    print("📁 Creando directorios...")
    
    directories = [
        "logs",
        "reports",
        "data",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def setup_environment():
    """Configura el archivo de entorno"""
    print("⚙️  Configurando entorno...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Archivo .env creado desde .env.example")
        print("ℹ️  Edite el archivo .env para agregar sus claves de API")
    else:
        print("ℹ️  Archivo .env ya existe o no se encontró .env.example")

def verify_installation():
    """Verifica que la instalación fue exitosa"""
    print("🔍 Verificando instalación...")
    
    try:
        # Verificar imports principales
        import streamlit
        import pandas
        import requests
        import plotly
        
        print("✅ Dependencias principales verificadas")
        
        # Verificar estructura de proyecto
        required_files = [
            "app.py",
            "config.py",
            "utils/logger.py",
            "utils/validators.py",
            "modules/domain_analyzer.py",
            "modules/email_analyzer.py",
            "modules/username_analyzer.py",
            "modules/social_analyzer.py"
        ]
        
        for file in required_files:
            if Path(file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file} no encontrado")
                
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        sys.exit(1)

def show_completion_message():
    """Muestra mensaje de instalación completada"""
    completion_message = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🎉 INSTALACIÓN COMPLETADA 🎉                         ║
║                                                                              ║
║  Para ejecutar OSINT-Nexus:                                                  ║
║                                                                              ║
║    1. Configure sus claves de API en el archivo .env                        ║
║    2. Ejecute: streamlit run app.py                                         ║
║    3. Abra su navegador en: http://localhost:8501                           ║
║                                                                              ║
║  Comandos útiles:                                                            ║
║    • streamlit run app.py --server.port 8080  (puerto personalizado)       ║
║    • streamlit run app.py --server.headless true  (sin navegador)          ║
║                                                                              ║
║  Documentación: README.md                                                    ║
║  Soporte: https://github.com/osint-nexus/osint-nexus                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(completion_message)

def main():
    """Función principal de instalación"""
    try:
        print_banner()
        check_python_version()
        check_system()
        create_directories()
        install_requirements()
        setup_environment()
        verify_installation()
        show_completion_message()
        
    except KeyboardInterrupt:
        print("\n⚠️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante la instalación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()