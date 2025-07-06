#!/usr/bin/env python3
"""
Script de instalación automática para el Buscador de Excel/CSV
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instalar las dependencias necesarias"""
    print("🔧 Instalando dependencias...")
    
    # Lista de paquetes requeridos
    paquetes = [
        'Flask==2.3.3',
        'pandas==2.0.3',
        'openpyxl==3.1.2',
        'xlrd==2.0.1',
        'Werkzeug==2.3.7',
        'numpy==1.24.3'
    ]
    
    for paquete in paquetes:
        try:
            print(f"📦 Instalando {paquete}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', paquete])
            print(f"✅ {paquete} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {paquete}: {e}")
            return False
    
    return True

def verificar_python():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"📍 Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def crear_estructura():
    """Crear la estructura de directorios necesaria"""
    print("📁 Creando estructura de directorios...")
    
    directorios = ['templates', 'uploads']
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✅ Directorio '{directorio}' creado")
        else:
            print(f"📁 Directorio '{directorio}' ya existe")

def verificar_archivos():
    """Verificar que los archivos necesarios existan"""
    print("📋 Verificando archivos necesarios...")
    
    archivos_necesarios = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'templates/search.html'
    ]
    
    faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
            print(f"❌ Archivo faltante: {archivo}")
        else:
            print(f"✅ Archivo encontrado: {archivo}")
    
    if faltantes:
        print(f"⚠️  Archivos faltantes: {', '.join(faltantes)}")
        return False
    
    return True

def main():
    """Función principal de instalación"""
    print("🔍 BUSCADOR DE EXCEL/CSV - INSTALACIÓN AUTOMÁTICA")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Crear estructura de directorios
    crear_estructura()
    
    # Verificar archivos
    if not verificar_archivos():
        print("❌ Algunos archivos necesarios están faltando")
        print("📋 Asegúrate de tener todos los archivos del proyecto")
        sys.exit(1)
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("❌ Error durante la instalación de dependencias")
        sys.exit(1)
    
    print("\n🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("📋 Pasos siguientes:")
    print("1. Ejecutar: python app.py")
    print("2. Abrir navegador en: http://localhost:5000")
    print("3. Cargar archivo Excel o CSV de ejemplo")
    print("4. ¡Comenzar a buscar!")
    print("\n📂 Archivo de ejemplo disponible: ejemplo_datos.csv")
    print("🔧 Para reinstalar: python instalar.py")

if __name__ == "__main__":
    main()