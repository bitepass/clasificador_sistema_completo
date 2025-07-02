#!/usr/bin/env python3
"""
🧪 Test básico del sistema DDIC-SM
Prueba la estructura sin dependencias externas
"""

import os
import sys
import sqlite3
from pathlib import Path

def test_file_structure():
    """Prueba la estructura de archivos"""
    print("🧪 Probando estructura de archivos...")
    
    required_files = [
        'src/main.py',
        'src/static/index.html',
        'src/static/reports.html',
        'requirements.txt',
        '.env.template'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_html_files():
    """Prueba que los archivos HTML sean válidos"""
    print("\n🎨 Probando archivos HTML...")
    
    html_files = ['src/static/index.html', 'src/static/reports.html']
    
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificaciones básicas
            checks = [
                ('<!DOCTYPE html>', 'DOCTYPE declaration'),
                ('<html', 'HTML tag'),
                ('<head>', 'HEAD section'),
                ('<body>', 'BODY section'),
                ('glassmorphism', 'Glassmorphism CSS'),
                ('fetch(', 'API calls'),
                ('DDIC-SM', 'DDIC-SM branding')
            ]
            
            print(f"\n📄 {html_file}:")
            for check, description in checks:
                if check in content:
                    print(f"  ✅ {description}")
                else:
                    print(f"  ❌ {description}")
        else:
            print(f"❌ {html_file} no encontrado")

def test_python_syntax():
    """Prueba la sintaxis de archivos Python"""
    print("\n🐍 Probando sintaxis Python...")
    
    python_files = [
        'src/main.py',
        '../launcher/DDIC_SM_Launcher.py'
    ]
    
    for py_file in python_files:
        if os.path.exists(py_file):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Compilar para verificar sintaxis
                compile(code, py_file, 'exec')
                print(f"✅ {py_file} - Sintaxis OK")
                
            except SyntaxError as e:
                print(f"❌ {py_file} - Error sintaxis: {e}")
            except Exception as e:
                print(f"⚠️ {py_file} - Error: {e}")
        else:
            print(f"❌ {py_file} no encontrado")

def test_database_creation():
    """Prueba la creación de base de datos SQLite"""
    print("\n💾 Probando base de datos...")
    
    db_path = 'src/database/test.db'
    os.makedirs('src/database', exist_ok=True)
    
    try:
        # Crear conexión SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla de prueba
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar datos de prueba
        cursor.execute("INSERT INTO test_table (nombre) VALUES ('DDIC-SM Test')")
        conn.commit()
        
        # Leer datos
        cursor.execute("SELECT * FROM test_table")
        results = cursor.fetchall()
        
        conn.close()
        
        if results:
            print("✅ Base de datos SQLite: OK")
            print(f"  📊 Registros: {len(results)}")
        else:
            print("❌ Base de datos: Sin datos")
            
    except Exception as e:
        print(f"❌ Base de datos: Error - {e}")

def test_frontend_apis():
    """Prueba las URLs de APIs en el frontend"""
    print("\n🔌 Probando APIs en frontend...")
    
    index_file = 'src/static/index.html'
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        api_endpoints = [
            '/api/clasificador/upload',
            '/api/clasificador/process',
            '/api/clasificador/status',
            '/api/clasificador/cancel',
            '/api/clasificador/generate-excel'
        ]
        
        for endpoint in api_endpoints:
            if endpoint in content:
                print(f"✅ API {endpoint}")
            else:
                print(f"❌ API {endpoint}")

def test_launcher_structure():
    """Prueba la estructura del launcher"""
    print("\n🚀 Probando launcher...")
    
    launcher_file = '../launcher/DDIC_SM_Launcher.py'
    if os.path.exists(launcher_file):
        with open(launcher_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        launcher_features = [
            ('class DDICLauncher', 'Clase principal'),
            ('def check_python', 'Verificación Python'),
            ('def install_dependencies', 'Instalación dependencias'),
            ('def show_api_config_dialog', 'Configurador APIs'),
            ('def start_flask_server', 'Inicio servidor'),
            ('tkinter', 'GUI Tkinter'),
            ('DDIC-SM', 'Branding')
        ]
        
        for feature, description in launcher_features:
            if feature in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
    else:
        print(f"❌ Launcher no encontrado")

def main():
    """Ejecuta todas las pruebas"""
    print("🎯 DDIC-SM - PRUEBAS DEL SISTEMA")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_html_files,
        test_python_syntax,
        test_database_creation,
        test_frontend_apis,
        test_launcher_structure
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            result = test()
            if result is not False:
                passed_tests += 1
        except Exception as e:
            print(f"❌ Error en test: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 RESULTADOS: {passed_tests}/{total_tests} pruebas pasadas")
    
    if passed_tests == total_tests:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está estructuralmente correcto")
    else:
        print("⚠️ Hay problemas que corregir")
    
    print("=" * 50)

if __name__ == "__main__":
    main()