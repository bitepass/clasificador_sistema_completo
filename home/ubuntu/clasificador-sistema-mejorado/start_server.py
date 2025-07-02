#!/usr/bin/env python3
"""
Script de inicio robusto para el Sistema Clasificador de Delitos
Maneja dependencias, configuración y inicialización automática
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Muestra el banner del sistema"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║            🎨 SISTEMA CLASIFICADOR DE DELITOS             ║
    ║                  Frontend Glassmorphism                   ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  🚀 Iniciando servidor Flask con frontend integrado...   ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def check_dependencies():
    """Verifica e instala dependencias si es necesario"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        'flask', 'flask-cors', 'flask-sqlalchemy', 'pandas', 
        'openpyxl', 'python-dotenv', 'google-generativeai', 'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - No encontrado")
    
    if missing_packages:
        print(f"\n📥 Instalando dependencias faltantes: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '--upgrade', 'pip'
            ])
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'requirements.txt'
            ])
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            sys.exit(1)

def setup_environment():
    """Configura el entorno y variables"""
    print("\n⚙️  Configurando entorno...")
    
    # Crear archivo .env si no existe
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("📝 Archivo .env creado desde .env.example")
            print("⚠️  IMPORTANTE: Configura tus API keys en el archivo .env")
        else:
            # Crear .env básico
            env_content = """# Configuración básica
SECRET_KEY=dev_secret_key_change_in_production
FLASK_ENV=development
FLASK_DEBUG=True
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            print("📝 Archivo .env básico creado")
    
    # Crear directorios necesarios
    dirs_to_create = ['logs', 'reports', 'src/database']
    for directory in dirs_to_create:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Directorio {directory} verificado")

def check_frontend_files():
    """Verifica que los archivos del frontend existan"""
    print("\n🎨 Verificando archivos del frontend...")
    
    frontend_files = [
        'src/static/index.html',
        'src/static/reports.html'
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - No encontrado")
            return False
    
    return True

def start_flask_server():
    """Inicia el servidor Flask"""
    print("\n🚀 Iniciando servidor Flask...")
    
    # Agregar el directorio actual al PYTHONPATH
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    try:
        # Importar y ejecutar la aplicación
        from src.main import app
        
        print("\n" + "="*60)
        print("🎉 ¡SERVIDOR INICIADO EXITOSAMENTE!")
        print("="*60)
        print("📱 Frontend Clasificador: http://localhost:5000")
        print("📊 Generador de Informes: http://localhost:5000/reports.html")
        print("🔧 API Base URL: http://localhost:5000/api")
        print("="*60)
        print("💡 Presiona Ctrl+C para detener el servidor")
        print("="*60)
        
        # Ejecutar la aplicación
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Evitar reinicios dobles
        )
        
    except ImportError as e:
        print(f"❌ Error importando la aplicación: {e}")
        print("🔍 Verifica que el archivo src/main.py exista y sea válido")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error iniciando el servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    try:
        print_banner()
        check_python_version()
        check_dependencies()
        setup_environment()
        
        if not check_frontend_files():
            print("\n❌ Error: Archivos del frontend no encontrados")
            print("🔧 Ejecuta el script de configuración del frontend primero")
            sys.exit(1)
        
        print("\n✅ Todas las verificaciones completadas")
        print("⏳ Iniciando en 2 segundos...")
        time.sleep(2)
        
        start_flask_server()
        
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
        print("🎉 ¡Gracias por usar el Sistema Clasificador de Delitos!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()