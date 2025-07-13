#!/usr/bin/env python3
"""
OSINT-NEXUS Setup Script
Automatiza la instalación y configuración inicial
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Mostrar banner de OSINT-NEXUS"""
    banner = f"""
{Colors.CYAN}
 ██████╗ ███████╗██╗███╗   ██╗████████╗    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██║   ██║███████╗██║██╔██╗ ██║   ██║       ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║   ██║╚════██║██║██║╚██╗██║   ██║       ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
╚██████╔╝███████║██║██║ ╚████║   ██║       ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Colors.END}
                    {Colors.BOLD}Plataforma de Inteligencia de Fuentes Abiertas{Colors.END}
"""
    print(banner)

def check_python_version():
    """Verificar versión de Python"""
    print(f"{Colors.BLUE}[*] Verificando versión de Python...{Colors.END}")
    
    if sys.version_info < (3, 8):
        print(f"{Colors.FAIL}[!] Python 3.8 o superior es requerido.{Colors.END}")
        print(f"    Tu versión actual es: Python {sys.version}")
        sys.exit(1)
    else:
        print(f"{Colors.GREEN}[✓] Python {sys.version.split()[0]} detectado{Colors.END}")

def create_virtual_environment():
    """Crear entorno virtual"""
    print(f"\n{Colors.BLUE}[*] Creando entorno virtual...{Colors.END}")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print(f"{Colors.GREEN}[✓] Entorno virtual creado exitosamente{Colors.END}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}[!] Error creando entorno virtual{Colors.END}")
        return False

def get_venv_python():
    """Obtener ruta al Python del entorno virtual"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def install_dependencies():
    """Instalar dependencias desde requirements.txt"""
    print(f"\n{Colors.BLUE}[*] Instalando dependencias...{Colors.END}")
    
    venv_python = get_venv_python()
    
    try:
        # Actualizar pip
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar requirements
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        
        print(f"{Colors.GREEN}[✓] Dependencias instaladas exitosamente{Colors.END}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}[!] Error instalando dependencias{Colors.END}")
        print(f"    {e}")
        return False

def setup_env_file():
    """Configurar archivo .env"""
    print(f"\n{Colors.BLUE}[*] Configurando archivo .env...{Colors.END}")
    
    if os.path.exists(".env"):
        print(f"{Colors.WARNING}[!] Archivo .env ya existe. No se sobrescribirá.{Colors.END}")
        return
    
    if os.path.exists(".env.example"):
        try:
            # Copiar .env.example a .env
            with open(".env.example", 'r') as src:
                with open(".env", 'w') as dst:
                    dst.write(src.read())
            
            print(f"{Colors.GREEN}[✓] Archivo .env creado desde .env.example{Colors.END}")
            print(f"{Colors.WARNING}[!] No olvides agregar tus claves API en el archivo .env{Colors.END}")
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error creando archivo .env: {e}{Colors.END}")
    else:
        print(f"{Colors.FAIL}[!] Archivo .env.example no encontrado{Colors.END}")

def create_directories():
    """Crear directorios necesarios"""
    print(f"\n{Colors.BLUE}[*] Creando directorios necesarios...{Colors.END}")
    
    directories = ['reports', 'temp', 'cache', 'downloads']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"{Colors.GREEN}[✓] Directorio '{directory}' creado/verificado{Colors.END}")

def print_next_steps():
    """Mostrar próximos pasos"""
    print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}[✓] ¡Instalación completada exitosamente!{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Próximos pasos:{Colors.END}")
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"""
1. Activa el entorno virtual:
   {Colors.CYAN}{activate_cmd}{Colors.END}

2. Configura tus claves API en el archivo .env:
   {Colors.CYAN}nano .env{Colors.END}  (o usa tu editor preferido)

3. Ejecuta OSINT-NEXUS:
   {Colors.CYAN}streamlit run app.py{Colors.END}

4. Abre tu navegador en:
   {Colors.CYAN}http://localhost:8501{Colors.END}
""")
    
    print(f"\n{Colors.WARNING}Recuerda:{Colors.END}")
    print("- Usa esta herramienta de manera ética y legal")
    print("- Respeta la privacidad de las personas")
    print("- Cumple con las leyes locales de protección de datos")
    
    print(f"\n{Colors.BOLD}¡Feliz investigación OSINT!{Colors.END} 🔍")

def main():
    """Función principal del setup"""
    print_banner()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("requirements.txt"):
        print(f"{Colors.FAIL}[!] Error: requirements.txt no encontrado.{Colors.END}")
        print("    Asegúrate de ejecutar este script desde el directorio osint-nexus/")
        sys.exit(1)
    
    # Ejecutar pasos de instalación
    check_python_version()
    
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    setup_env_file()
    create_directories()
    
    # Mostrar instrucciones finales
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Instalación cancelada por el usuario{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Error inesperado: {e}{Colors.END}")
        sys.exit(1)