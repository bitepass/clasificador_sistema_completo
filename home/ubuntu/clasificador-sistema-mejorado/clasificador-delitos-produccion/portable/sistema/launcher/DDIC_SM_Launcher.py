#!/usr/bin/env python3
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
                           "Se requiere Python 3.7+\n"
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
                           "El Clasificador de Delitos está funcionando\n"
                           "Acceso: http://localhost:5000\n"
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
