#!/usr/bin/env python3
"""
Script de ejecución para el Buscador de Excel/CSV
"""

import subprocess
import sys
import os
import webbrowser
import time

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencias = ['flask', 'pandas', 'openpyxl', 'xlrd', 'werkzeug', 'numpy']
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            print("🔧 Ejecuta primero: python instalar.py")
            return False
    
    return True

def abrir_navegador():
    """Abrir navegador web automáticamente"""
    print("🌐 Abriendo navegador web...")
    time.sleep(2)  # Esperar a que el servidor inicie
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Navegador abierto en: http://localhost:5000")
    except Exception as e:
        print(f"⚠️  No se pudo abrir el navegador automáticamente: {e}")
        print("📋 Abre manualmente: http://localhost:5000")

def main():
    """Función principal de ejecución"""
    print("🔍 BUSCADOR DE EXCEL/CSV - INICIANDO SERVIDOR")
    print("=" * 50)
    
    # Verificar que app.py existe
    if not os.path.exists('app.py'):
        print("❌ No se encontró app.py")
        print("📋 Asegúrate de estar en el directorio correcto")
        sys.exit(1)
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    print("\n🚀 Iniciando servidor web...")
    print("📋 Instrucciones:")
    print("   • El navegador se abrirá automáticamente")
    print("   • Si no se abre, ve a: http://localhost:5000")
    print("   • Presiona Ctrl+C para detener el servidor")
    print("   • Usa ejemplo_datos.csv para pruebas")
    print("=" * 50)
    
    # Abrir navegador en segundo plano
    import threading
    browser_thread = threading.Thread(target=abrir_navegador)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Ejecutar la aplicación
    try:
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido por el usuario")
        print("👋 ¡Gracias por usar el Buscador de Excel/CSV!")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()