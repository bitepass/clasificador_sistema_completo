#!/usr/bin/env python3
"""
🚀 DDIC-SM Clasificador de Delitos - Constructor de Instalador Completo
Crea una versión de producción sin límites, completamente funcional
"""
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
import json

class ProductionBuilder:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.production_dir = self.base_dir / "clasificador-delitos-produccion"
        self.build_dir = self.production_dir / "build"
        self.installer_dir = self.production_dir / "installer"
        
    def print_banner(self):
        banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                🏢 DDIC-SM CLASIFICADOR DE DELITOS                ║
║                     🚀 CONSTRUCTOR DE PRODUCCIÓN                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  📦 Creando instalador profesional completo                      ║
║  💾 Sin límites - Todas las funcionalidades incluidas            ║
║  🌐 Portable + Instalable + Auto-configuración                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def create_directory_structure(self):
        """Crea la estructura de directorios de producción"""
        print("\n📁 Creando estructura de directorios...")
        
        directories = [
            self.production_dir,
            self.build_dir,
            self.installer_dir,
            self.build_dir / "app",
            self.build_dir / "app" / "src",
            self.build_dir / "app" / "data",
            self.build_dir / "app" / "logs",
            self.build_dir / "app" / "reports",
            self.build_dir / "app" / "backups",
            self.build_dir / "python-portable",
            self.build_dir / "launcher",
            self.installer_dir / "assets",
            self.installer_dir / "scripts"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ {directory}")
    
    def copy_application_files(self):
        """Copia y optimiza los archivos de la aplicación"""
        print("\n📋 Copiando archivos de la aplicación...")
        
        # Copiar estructura principal
        src_files = [
            ("src/", "app/src/"),
            ("requirements.txt", "app/"),
            (".env.example", "app/.env.template"),
            ("README.md", "app/"),
            ("FRONTEND_README.md", "app/")
        ]
        
        for src, dst in src_files:
            src_path = self.base_dir / src
            dst_path = self.build_dir / dst
            
            if src_path.is_dir():
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"📂 {src} → {dst}")
            elif src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"📄 {src} → {dst}")
    
    def create_production_launcher(self):
        """Crea el launcher optimizado para producción"""
        print("\n🚀 Creando launcher de producción...")
        
        launcher_code = '''#!/usr/bin/env python3
"""
🎯 DDIC-SM Clasificador de Delitos - Launcher de Producción
Launcher inteligente que maneja toda la inicialización
"""
import os
import sys
import subprocess
import time
import webbrowser
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import json
import socket

class DDICLauncher:
    def __init__(self):
        self.app_dir = Path(__file__).parent / "app"
        self.python_dir = Path(__file__).parent / "python-portable"
        self.config_file = self.app_dir / "config.json"
        self.server_process = None
        
    def check_python(self):
        """Verifica y configura Python"""
        # Intentar usar Python del sistema primero
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return sys.executable
        except:
            pass
        
        # Buscar Python portable
        portable_python = self.python_dir / "python.exe"
        if portable_python.exists():
            return str(portable_python)
        
        # Si no hay Python, mostrar mensaje
        messagebox.showerror("Python No Encontrado", 
                           "Se requiere Python 3.7+\\n"
                           "El instalador debería incluir Python portable.")
        return None
    
    def install_dependencies(self, python_exe):
        """Instala dependencias si es necesario"""
        requirements_file = self.app_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                subprocess.run([python_exe, "-m", "pip", "install", "-r", 
                              str(requirements_file)], check=True, 
                             capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return True
    
    def check_apis_configured(self):
        """Verifica si las APIs están configuradas"""
        env_file = self.app_dir / ".env"
        if not env_file.exists():
            return False
        
        with open(env_file, 'r') as f:
            content = f.read()
            return ("your_gemini_api_key_here" not in content and 
                   "your_openai_api_key_here" not in content)
    
    def show_api_config_dialog(self):
        """Muestra diálogo para configurar APIs"""
        config_window = tk.Toplevel()
        config_window.title("DDIC-SM - Configuración de APIs")
        config_window.geometry("500x400")
        config_window.resizable(False, False)
        
        # Centrar ventana
        config_window.transient()
        config_window.grab_set()
        
        # Contenido
        ttk.Label(config_window, text="🔑 Configuración de APIs", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        ttk.Label(config_window, text="Para usar la clasificación automática, "
                 "configure sus claves de API:").pack(pady=5)
        
        # Gemini API
        ttk.Label(config_window, text="🤖 Gemini API Key:").pack(anchor="w", padx=20, pady=(10,0))
        gemini_var = tk.StringVar()
        gemini_entry = ttk.Entry(config_window, textvariable=gemini_var, width=60, show="*")
        gemini_entry.pack(padx=20, pady=5)
        
        # OpenAI API
        ttk.Label(config_window, text="🧠 OpenAI API Key:").pack(anchor="w", padx=20, pady=(10,0))
        openai_var = tk.StringVar()
        openai_entry = ttk.Entry(config_window, textvariable=openai_var, width=60, show="*")
        openai_entry.pack(padx=20, pady=5)
        
        # Botones
        button_frame = ttk.Frame(config_window)
        button_frame.pack(pady=20)
        
        def save_config():
            gemini_key = gemini_var.get().strip()
            openai_key = openai_var.get().strip()
            
            if gemini_key or openai_key:
                self.save_api_config(gemini_key, openai_key)
                config_window.destroy()
                self.start_application()
            else:
                messagebox.showwarning("Configuración Incompleta", 
                                     "Debe configurar al menos una API key.")
        
        def skip_config():
            messagebox.showinfo("Modo Limitado", 
                               "El sistema funcionará con clasificación por reglas únicamente.")
            config_window.destroy()
            self.start_application()
        
        ttk.Button(button_frame, text="💾 Guardar y Continuar", 
                  command=save_config).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⏭️ Omitir", 
                  command=skip_config).pack(side="left", padx=5)
    
    def save_api_config(self, gemini_key, openai_key):
        """Guarda la configuración de APIs"""
        env_template = self.app_dir / ".env.template"
        env_file = self.app_dir / ".env"
        
        if env_template.exists():
            with open(env_template, 'r') as f:
                content = f.read()
        else:
            content = """# DDIC-SM Clasificador de Delitos - Configuración
SECRET_KEY=ddic_sm_secret_key_2024
FLASK_ENV=production
FLASK_DEBUG=False
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
"""
        
        # Reemplazar claves
        if gemini_key:
            content = content.replace("your_gemini_api_key_here", gemini_key)
        if openai_key:
            content = content.replace("your_openai_api_key_here", openai_key)
        
        with open(env_file, 'w') as f:
            f.write(content)
    
    def is_port_in_use(self, port):
        """Verifica si un puerto está en uso"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def start_flask_server(self, python_exe):
        """Inicia el servidor Flask"""
        main_py = self.app_dir / "src" / "main.py"
        if main_py.exists():
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.app_dir)
            
            self.server_process = subprocess.Popen(
                [python_exe, str(main_py)],
                cwd=str(self.app_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        return False
    
    def wait_for_server(self, timeout=30):
        """Espera a que el servidor esté listo"""
        for _ in range(timeout):
            if self.is_port_in_use(5000):
                return True
            time.sleep(1)
        return False
    
    def open_browser(self):
        """Abre el navegador con la aplicación"""
        webbrowser.open("http://localhost:5000")
    
    def show_loading_dialog(self):
        """Muestra diálogo de carga"""
        loading_window = tk.Toplevel()
        loading_window.title("DDIC-SM - Iniciando...")
        loading_window.geometry("400x200")
        loading_window.resizable(False, False)
        
        # Centrar ventana
        loading_window.transient()
        loading_window.grab_set()
        
        ttk.Label(loading_window, text="🚀 DDIC-SM Clasificador de Delitos", 
                 font=("Arial", 12, "bold")).pack(pady=20)
        
        progress = ttk.Progressbar(loading_window, mode='indeterminate')
        progress.pack(pady=10, padx=50, fill="x")
        progress.start()
        
        status_label = ttk.Label(loading_window, text="Iniciando servidor...")
        status_label.pack(pady=10)
        
        return loading_window, status_label
    
    def start_application(self):
        """Inicia la aplicación completa"""
        python_exe = self.check_python()
        if not python_exe:
            return
        
        # Mostrar ventana de carga
        loading_window, status_label = self.show_loading_dialog()
        
        def start_process():
            try:
                # Instalar dependencias
                status_label.config(text="Verificando dependencias...")
                if not self.install_dependencies(python_exe):
                    messagebox.showerror("Error", "Error instalando dependencias")
                    loading_window.destroy()
                    return
                
                # Iniciar servidor
                status_label.config(text="Iniciando servidor Flask...")
                if not self.start_flask_server(python_exe):
                    messagebox.showerror("Error", "Error iniciando servidor")
                    loading_window.destroy()
                    return
                
                # Esperar a que esté listo
                status_label.config(text="Esperando conexión...")
                if self.wait_for_server():
                    loading_window.destroy()
                    self.open_browser()
                    self.show_system_tray()
                else:
                    messagebox.showerror("Error", "Timeout esperando servidor")
                    loading_window.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
                loading_window.destroy()
        
        threading.Thread(target=start_process, daemon=True).start()
    
    def show_system_tray(self):
        """Muestra información en system tray"""
        messagebox.showinfo("DDIC-SM Activo", 
                           "El Clasificador de Delitos está funcionando\\n"
                           "Acceso: http://localhost:5000\\n"
                           "Cierre esta ventana para finalizar.")
        
        # Terminar servidor al cerrar
        if self.server_process:
            self.server_process.terminate()
    
    def run(self):
        """Ejecuta el launcher"""
        root = tk.Tk()
        root.title("DDIC-SM Launcher")
        root.geometry("400x300")
        
        # Logo y título
        ttk.Label(root, text="🏢 DDIC-SM", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(root, text="Clasificador de Delitos", font=("Arial", 12)).pack()
        ttk.Label(root, text="Subtte Carrizo Jorge / Osa Grandolio Gabriel", 
                 font=("Arial", 8)).pack(pady=5)
        
        # Verificar configuración
        if not self.check_apis_configured():
            ttk.Label(root, text="⚠️ Configuración de APIs requerida", 
                     foreground="orange").pack(pady=10)
            ttk.Button(root, text="🔑 Configurar APIs", 
                      command=lambda: [root.withdraw(), self.show_api_config_dialog()]).pack(pady=5)
        
        ttk.Button(root, text="🚀 Iniciar Sistema", 
                  command=lambda: [root.withdraw(), self.start_application()]).pack(pady=10)
        
        ttk.Button(root, text="❌ Salir", command=root.quit).pack(pady=5)
        
        root.mainloop()

if __name__ == "__main__":
    launcher = DDICLauncher()
    launcher.run()
'''
        
        launcher_file = self.build_dir / "launcher" / "DDIC_SM_Launcher.py"
        with open(launcher_file, 'w', encoding='utf-8') as f:
            f.write(launcher_code)
        
        print(f"✅ Launcher creado: {launcher_file}")
    
    def create_installer_script(self):
        """Crea el script de Inno Setup"""
        print("\n📦 Creando script de Inno Setup...")
        
        inno_script = f'''
; 🏢 DDIC-SM Clasificador de Delitos - Script de Instalación
; Contactos: Subtte Carrizo Jorge / Osa Grandolio Gabriel

[Setup]
AppName=DDIC-SM Clasificador de Delitos
AppVersion=1.0.0
AppPublisher=DDIC-SM
AppContact=Subtte Carrizo Jorge / Osa Grandolio Gabriel
DefaultDirName={{pf}}\\DDIC-SM\\Clasificador-Delitos
DefaultGroupName=DDIC-SM
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=DDIC-SM-Clasificador-Delitos-Setup
SetupIconFile=assets\\logo.ico
UninstallDisplayIcon={{app}}\\launcher\\DDIC_SM_Launcher.exe
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "build\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\DDIC-SM Clasificador de Delitos"; Filename: "{{app}}\\launcher\\DDIC_SM_Launcher.exe"; WorkingDir: "{{app}}"
Name: "{{group}}\\{{cm:UninstallProgram,DDIC-SM Clasificador de Delitos}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\DDIC-SM Clasificador de Delitos"; Filename: "{{app}}\\launcher\\DDIC_SM_Launcher.exe"; WorkingDir: "{{app}}"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\DDIC-SM Clasificador"; Filename: "{{app}}\\launcher\\DDIC_SM_Launcher.exe"; WorkingDir: "{{app}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\launcher\\DDIC_SM_Launcher.exe"; Description: "{{cm:LaunchProgram,DDIC-SM Clasificador}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('🏢 DDIC-SM Clasificador de Delitos' + #13#10 + 
         'Sistema de clasificación automática de hechos delictivos' + #13#10 + #13#10 +
         'Contactos:' + #13#10 +
         '• Subtte Carrizo Jorge' + #13#10 +
         '• Osa Grandolio Gabriel', mbInformation, MB_OK);
end;
'''
        
        script_file = self.installer_dir / "setup.iss"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(inno_script)
        
        print(f"✅ Script de Inno Setup creado: {script_file}")
    
    def create_portable_package(self):
        """Crea un paquete portable"""
        print("\n💾 Creando paquete portable...")
        
        portable_dir = self.production_dir / "portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Crear script portable
        portable_script = '''@echo off
title DDIC-SM Clasificador de Delitos - Modo Portable
echo 🏢 DDIC-SM Clasificador de Delitos
echo 💾 Modo Portable - Sin instalación requerida
echo.
echo Iniciando sistema...
cd /d "%~dp0"
python launcher\\DDIC_SM_Launcher.py
pause
'''
        
        with open(portable_dir / "EJECUTAR_DDIC_SM.bat", 'w') as f:
            f.write(portable_script)
        
        # Copiar archivos
        shutil.copytree(self.build_dir, portable_dir / "sistema", dirs_exist_ok=True)
        
        print(f"✅ Paquete portable creado: {portable_dir}")
    
    def create_documentation(self):
        """Crea documentación completa"""
        print("\n📚 Creando documentación...")
        
        readme_content = '''# 🏢 DDIC-SM Clasificador de Delitos - Versión Producción

## 🎯 Sistema Completo - Sin Limitaciones

### 📦 Instalación
1. Ejecutar `DDIC-SM-Clasificador-Delitos-Setup.exe`
2. Seguir el asistente de instalación
3. Configurar APIs en primer uso
4. ¡Listo para usar!

### 💾 Modo Portable
1. Descomprimir carpeta `portable`
2. Ejecutar `EJECUTAR_DDIC_SM.bat`
3. Configurar APIs si es necesario
4. Sistema funcionando desde cualquier ubicación

### 🔑 Configuración de APIs
- **Gemini API:** https://makersuite.google.com/app/apikey
- **OpenAI API:** https://platform.openai.com/api-keys

### 🌐 Acceso al Sistema
- **URL:** http://localhost:5000
- **Clasificador:** Página principal
- **Informes:** /reports.html

### 👥 Contactos
- **Subtte Carrizo Jorge**
- **Osa Grandolio Gabriel**

### 📱 Características Completas
✅ Clasificación automática con IA
✅ Procesamiento de archivos Excel
✅ Generación de informes profesionales
✅ Interfaz glassmorphism moderna
✅ Base de datos persistente
✅ Modo portable y tradicional
✅ Compatible Windows 10/11
✅ Auto-configuración inteligente
'''
        
        readme_file = self.production_dir / "README_PRODUCCION.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Documentación creada: {readme_file}")
    
    def build_production(self):
        """Construye la versión de producción completa"""
        try:
            self.print_banner()
            
            print("🏗️ Iniciando construcción de versión de producción...")
            
            # Crear estructura
            self.create_directory_structure()
            
            # Copiar archivos
            self.copy_application_files()
            
            # Crear launcher
            self.create_production_launcher()
            
            # Crear instalador
            self.create_installer_script()
            
            # Crear portable
            self.create_portable_package()
            
            # Crear documentación
            self.create_documentation()
            
            print("\n" + "="*70)
            print("🎉 ¡CONSTRUCCIÓN COMPLETADA EXITOSAMENTE!")
            print("="*70)
            print(f"📂 Directorio de producción: {self.production_dir}")
            print(f"📦 Script instalador: {self.installer_dir / 'setup.iss'}")
            print(f"💾 Paquete portable: {self.production_dir / 'portable'}")
            print("="*70)
            print("📋 PRÓXIMOS PASOS:")
            print("1. Instalar Inno Setup: https://jrsoftware.org/isinfo.php")
            print("2. Abrir setup.iss con Inno Setup")
            print("3. Compilar para generar el .exe final")
            print("4. ¡Distribuir el instalador!")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ Error durante la construcción: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    builder = ProductionBuilder()
    builder.build_production()