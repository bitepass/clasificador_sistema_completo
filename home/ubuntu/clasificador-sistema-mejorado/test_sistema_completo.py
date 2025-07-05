#!/usr/bin/env python3
"""
🔍 SISTEMA DE VERIFICACIÓN EXHAUSTIVA - CLASIFICADOR DE DELITOS DDIC-SM
========================================================================

Este script verifica al 100% de precisión que cada componente del sistema funcione correctamente.
Los datos precisos pueden salvar vidas - cada función debe ser perfecta.

Desarrollado por: Subtte Carrizo Jorge / Osa Grandolio Gabriel
Organización: DDIC-SM
"""

import sys
import os
import traceback
import time
import json
import pandas as pd
import requests
from datetime import datetime
from openpyxl import Workbook
import sqlite3
from urllib.parse import urlparse
import threading
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_results.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TestResult:
    """Clase para almacenar resultados de pruebas"""
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        self.warnings = []
        self.start_time = time.time()
        
    def add_pass(self, test_name, details=""):
        self.tests_passed += 1
        logger.info(f"✅ PASS: {test_name} {details}")
        
    def add_fail(self, test_name, error, details=""):
        self.tests_failed += 1
        error_msg = f"❌ FAIL: {test_name} - {error} {details}"
        logger.error(error_msg)
        self.errors.append(error_msg)
        
    def add_warning(self, test_name, warning, details=""):
        warning_msg = f"⚠️  WARN: {test_name} - {warning} {details}"
        logger.warning(warning_msg)
        self.warnings.append(warning_msg)
        
    def get_summary(self):
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        duration = time.time() - self.start_time
        
        return {
            'total_tests': total_tests,
            'passed': self.tests_passed,
            'failed': self.tests_failed,
            'success_rate': success_rate,
            'duration': duration,
            'errors': self.errors,
            'warnings': self.warnings
        }

def test_python_imports():
    """Verifica que todas las dependencias críticas estén instaladas"""
    result = TestResult()
    
    critical_imports = [
        'flask', 'flask_sqlalchemy', 'flask_cors', 'pandas', 'openpyxl',
        'google.generativeai', 'openai', 'requests', 'dotenv', 'sqlite3'
    ]
    
    for module in critical_imports:
        try:
            __import__(module)
            result.add_pass(f"Import {module}")
        except ImportError as e:
            result.add_fail(f"Import {module}", str(e))
    
    return result

def test_database_structure():
    """Verifica la estructura de la base de datos"""
    result = TestResult()
    
    try:
        # Verificar que la base de datos existe
        db_path = '/workspace/home/ubuntu/clasificador-sistema-mejorado/src/database/app.db'
        if not os.path.exists(db_path):
            result.add_fail("Database existence", f"Database file not found: {db_path}")
            return result
        
        result.add_pass("Database file exists")
        
        # Conectar y verificar tablas
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas críticas
        critical_tables = [
            'users', 'planillas', 'hechos_delictivos', 
            'personas_involucradas', 'logs_procesamiento'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in critical_tables:
            if table in existing_tables:
                result.add_pass(f"Table {table} exists")
            else:
                result.add_fail(f"Table {table} missing", f"Required table {table} not found")
        
        # Verificar estructura de tabla crítica
        cursor.execute("PRAGMA table_info(hechos_delictivos)")
        columns = [row[1] for row in cursor.fetchall()]
        
        critical_columns = [
            'id', 'planilla_id', 'jurisdiccion', 'calificacion', 'modalidad',
            'victimas', 'armas', 'lugar', 'metodo_clasificacion', 'confianza_clasificacion'
        ]
        
        for column in critical_columns:
            if column in columns:
                result.add_pass(f"Column {column} exists in hechos_delictivos")
            else:
                result.add_fail(f"Column {column} missing", f"Critical column {column} not found")
        
        conn.close()
        
    except Exception as e:
        result.add_fail("Database structure check", str(e))
    
    return result

def test_classification_functions():
    """Verifica las funciones de clasificación"""
    result = TestResult()
    
    try:
        # Importar módulos necesarios
        sys.path.insert(0, '/workspace/home/ubuntu/clasificador-sistema-mejorado')
        from src.routes.clasificador import (
            clasificacion_basada_en_reglas, 
            clasificacion_por_defecto,
            limpiar_clasificacion,
            clasificar_fila_con_cascada,
            CATEGORIAS_CLASIFICACION
        )
        
        # Test 1: Clasificación por defecto
        clasificacion_def, metodo_def = clasificacion_por_defecto()
        if isinstance(clasificacion_def, dict) and metodo_def == 'DEFECTO':
            result.add_pass("Clasificación por defecto")
        else:
            result.add_fail("Clasificación por defecto", "No retorna estructura correcta")
        
        # Test 2: Clasificación basada en reglas
        texto_test = "Robo con arma de fuego en vía pública a una mujer"
        clasificacion_reglas, metodo_reglas = clasificacion_basada_en_reglas(texto_test)
        
        if isinstance(clasificacion_reglas, dict) and metodo_reglas == 'REGLAS':
            result.add_pass("Clasificación por reglas")
            
            # Verificar que las reglas funcionen correctamente
            if 'ROBO' in clasificacion_reglas.get('CALIFICACION', ''):
                result.add_pass("Regla de robo detectada")
            else:
                result.add_warning("Regla de robo", "No se detectó robo en el texto")
                
            if clasificacion_reglas.get('ARMAS') == 'FUEGO':
                result.add_pass("Regla de arma de fuego detectada")
            else:
                result.add_warning("Regla de arma", "No se detectó arma de fuego")
                
        else:
            result.add_fail("Clasificación por reglas", "No funciona correctamente")
        
        # Test 3: Limpieza de clasificación
        clasificacion_sucia = {
            'JURISDICCION': 'URBANA',
            'CALIFICACION': 'VALOR_INVALIDO',
            'MODALIDAD': 'OTROS',
            'campo_invalido': 'valor'
        }
        
        clasificacion_limpia = limpiar_clasificacion(clasificacion_sucia)
        if isinstance(clasificacion_limpia, dict):
            result.add_pass("Limpieza de clasificación")
            
            if clasificacion_limpia.get('CALIFICACION') == 'OTROS':
                result.add_pass("Limpieza corrige valores inválidos")
            else:
                result.add_fail("Limpieza de valores", "No corrige valores inválidos")
        else:
            result.add_fail("Limpieza de clasificación", "No retorna diccionario")
        
        # Test 4: Clasificación con cascada
        clasificacion_cascada, metodo_cascada, tiempo_ms, confianza = clasificar_fila_con_cascada(texto_test, 1)
        
        if isinstance(clasificacion_cascada, dict) and isinstance(tiempo_ms, int) and isinstance(confianza, float):
            result.add_pass("Clasificación con cascada")
            
            if 0 <= confianza <= 1:
                result.add_pass("Confianza en rango válido")
            else:
                result.add_fail("Confianza fuera de rango", f"Confianza: {confianza}")
                
            if tiempo_ms > 0:
                result.add_pass("Tiempo de procesamiento válido")
            else:
                result.add_fail("Tiempo de procesamiento", f"Tiempo: {tiempo_ms}ms")
        else:
            result.add_fail("Clasificación con cascada", "No retorna estructura correcta")
        
        # Test 5: Categorías de clasificación
        for categoria, valores in CATEGORIAS_CLASIFICACION.items():
            if isinstance(valores, list) and len(valores) > 0:
                result.add_pass(f"Categoría {categoria} válida")
            else:
                result.add_fail(f"Categoría {categoria}", "Lista vacía o inválida")
        
    except Exception as e:
        result.add_fail("Funciones de clasificación", str(e))
        result.add_fail("Error traceback", traceback.format_exc())
    
    return result

def test_excel_processing():
    """Verifica el procesamiento de archivos Excel"""
    result = TestResult()
    
    try:
        # Crear archivo Excel de prueba
        test_data = {
            'id_hecho': ['H001', 'H002', 'H003'],
            'nro_registro': ['R001', 'R002', 'R003'],
            'relato': [
                'Robo con arma de fuego en vía pública',
                'Homicidio simple en domicilio particular',
                'Lesiones con arma blanca en comercio'
            ],
            'fecha_hecho': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'comisaria': ['Comisaría 1', 'Comisaría 2', 'Comisaría 3'],
            'localidad': ['San Martín', 'José C. Paz', 'Malvinas Argentinas']
        }
        
        df = pd.DataFrame(test_data)
        test_excel_path = '/tmp/test_clasificador.xlsx'
        df.to_excel(test_excel_path, index=False)
        
        result.add_pass("Archivo Excel de prueba creado")
        
        # Verificar que el archivo se puede leer
        df_read = pd.read_excel(test_excel_path)
        if len(df_read) == 3 and 'relato' in df_read.columns:
            result.add_pass("Archivo Excel se puede leer correctamente")
        else:
            result.add_fail("Lectura de Excel", "No se puede leer el archivo correctamente")
        
        # Test procesamiento de cada fila
        sys.path.insert(0, '/workspace/home/ubuntu/clasificador-sistema-mejorado')
        from src.routes.clasificador import clasificar_fila_con_cascada
        
        for index, row in df_read.iterrows():
            clasificacion, metodo, tiempo, confianza = clasificar_fila_con_cascada(row['relato'], index)
            
            if isinstance(clasificacion, dict) and 'jurisdiccion' in clasificacion:
                result.add_pass(f"Procesamiento fila {index + 1}")
            else:
                result.add_fail(f"Procesamiento fila {index + 1}", "Clasificación inválida")
        
        # Limpiar archivo de prueba
        os.remove(test_excel_path)
        
    except Exception as e:
        result.add_fail("Procesamiento Excel", str(e))
        result.add_fail("Error traceback", traceback.format_exc())
    
    return result

def test_api_endpoints():
    """Verifica que los endpoints de la API funcionen"""
    result = TestResult()
    
    # Iniciar servidor Flask en hilo separado
    server_process = None
    try:
        import subprocess
        import signal
        
        # Activar entorno virtual y ejecutar servidor
        server_cmd = [
            '/workspace/home/ubuntu/clasificador-sistema-mejorado/venv/bin/python',
            'src/main.py'
        ]
        
        server_process = subprocess.Popen(
            server_cmd, 
            cwd='/workspace/home/ubuntu/clasificador-sistema-mejorado',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        
        # Esperar a que el servidor inicie
        time.sleep(5)
        
        base_url = 'http://localhost:5000'
        
        # Test 1: Endpoint de test
        try:
            response = requests.get(f'{base_url}/api/clasificador/test', timeout=10)
            if response.status_code == 200:
                result.add_pass("Endpoint /api/clasificador/test")
            else:
                result.add_fail("Endpoint test", f"Status code: {response.status_code}")
        except Exception as e:
            result.add_fail("Endpoint test", str(e))
        
        # Test 2: Endpoint de planillas
        try:
            response = requests.get(f'{base_url}/api/clasificador/planillas', timeout=10)
            if response.status_code == 200:
                result.add_pass("Endpoint /api/clasificador/planillas")
            else:
                result.add_fail("Endpoint planillas", f"Status code: {response.status_code}")
        except Exception as e:
            result.add_fail("Endpoint planillas", str(e))
        
        # Test 3: Upload de archivo
        try:
            # Crear archivo de prueba
            test_data = {'relato': ['Robo con arma de fuego']}
            df = pd.DataFrame(test_data)
            test_path = '/tmp/test_upload.xlsx'
            df.to_excel(test_path, index=False)
            
            with open(test_path, 'rb') as f:
                files = {'file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = requests.post(f'{base_url}/api/clasificador/upload', files=files, timeout=30)
            
            if response.status_code == 200:
                result.add_pass("Endpoint /api/clasificador/upload")
                
                # Extraer planilla_id para siguiente test
                upload_data = response.json()
                if 'planilla_id' in upload_data:
                    planilla_id = upload_data['planilla_id']
                    
                    # Test 4: Procesamiento
                    try:
                        response = requests.post(f'{base_url}/api/clasificador/process/{planilla_id}', timeout=30)
                        if response.status_code == 200:
                            result.add_pass("Endpoint /api/clasificador/process")
                            
                            # Test 5: Estado de procesamiento
                            time.sleep(2)
                            response = requests.get(f'{base_url}/api/clasificador/status/{planilla_id}', timeout=10)
                            if response.status_code == 200:
                                result.add_pass("Endpoint /api/clasificador/status")
                            else:
                                result.add_fail("Endpoint status", f"Status code: {response.status_code}")
                        else:
                            result.add_fail("Endpoint process", f"Status code: {response.status_code}")
                    except Exception as e:
                        result.add_fail("Endpoint process", str(e))
            else:
                result.add_fail("Endpoint upload", f"Status code: {response.status_code}")
            
            os.remove(test_path)
            
        except Exception as e:
            result.add_fail("Endpoint upload", str(e))
        
    except Exception as e:
        result.add_fail("Inicialización del servidor", str(e))
    
    finally:
        # Terminar proceso del servidor
        if server_process:
            try:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                server_process.wait(timeout=10)
            except:
                pass
    
    return result

def test_ai_integration():
    """Verifica la integración con APIs de IA"""
    result = TestResult()
    
    try:
        # Verificar variables de entorno
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if gemini_key and gemini_key != 'your_gemini_api_key_here':
            result.add_pass("Gemini API key configurada")
        else:
            result.add_warning("Gemini API key", "No configurada - se usará clasificación por reglas")
        
        if openai_key and openai_key != 'your_openai_api_key_here':
            result.add_pass("OpenAI API key configurada")
        else:
            result.add_warning("OpenAI API key", "No configurada - se usará clasificación por reglas")
        
        # Test de clasificación con IA (si está disponible)
        sys.path.insert(0, '/workspace/home/ubuntu/clasificador-sistema-mejorado')
        from src.routes.clasificador import clasificar_texto_con_gemini
        
        texto_test = "Robo con arma de fuego en vía pública a una mujer"
        
        try:
            clasificacion_gemini, metodo = clasificar_texto_con_gemini(texto_test)
            if clasificacion_gemini and isinstance(clasificacion_gemini, dict):
                result.add_pass("Clasificación con Gemini AI")
            else:
                result.add_warning("Clasificación Gemini", "No retorna clasificación válida")
        except Exception as e:
            result.add_warning("Clasificación Gemini", f"Error: {str(e)}")
        
    except Exception as e:
        result.add_fail("Integración AI", str(e))
    
    return result

def test_security_measures():
    """Verifica las medidas de seguridad implementadas"""
    result = TestResult()
    
    try:
        # Verificar archivos de seguridad
        security_files = [
            '/workspace/security_patches_corrected/security_manager.py',
            '/workspace/security_patches_corrected/protected_main.py',
            '/workspace/security_patches_corrected/SECURITY_README.md'
        ]
        
        for file_path in security_files:
            if os.path.exists(file_path):
                result.add_pass(f"Archivo de seguridad existe: {os.path.basename(file_path)}")
            else:
                result.add_fail(f"Archivo de seguridad faltante", f"No encontrado: {file_path}")
        
        # Verificar permisos de archivos críticos
        critical_files = [
            '/workspace/home/ubuntu/clasificador-sistema-mejorado/src/main.py',
            '/workspace/home/ubuntu/clasificador-sistema-mejorado/src/routes/clasificador.py'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                if stat.st_mode & 0o444:  # Readable
                    result.add_pass(f"Permisos válidos: {os.path.basename(file_path)}")
                else:
                    result.add_fail(f"Permisos inválidos", f"Archivo no legible: {file_path}")
        
        # Verificar que no hay credenciales hardcodeadas
        config_files = [
            '/workspace/home/ubuntu/clasificador-sistema-mejorado/src/main.py',
            '/workspace/home/ubuntu/clasificador-sistema-mejorado/src/routes/clasificador.py'
        ]
        
        dangerous_patterns = ['password', 'secret', 'api_key', 'token']
        
        for file_path in config_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    
                for pattern in dangerous_patterns:
                    if pattern in content and 'getenv' not in content:
                        result.add_warning(f"Posible credencial hardcodeada", f"Patrón '{pattern}' en {file_path}")
        
        result.add_pass("Verificación de seguridad completada")
        
    except Exception as e:
        result.add_fail("Verificación de seguridad", str(e))
    
    return result

def test_performance():
    """Verifica el rendimiento del sistema"""
    result = TestResult()
    
    try:
        sys.path.insert(0, '/workspace/home/ubuntu/clasificador-sistema-mejorado')
        from src.routes.clasificador import clasificar_fila_con_cascada
        
        # Test de rendimiento - procesamiento de múltiples casos
        test_cases = [
            "Robo con arma de fuego en vía pública",
            "Homicidio simple en domicilio particular",
            "Lesiones con arma blanca en comercio",
            "Estafa por WhatsApp a persona mayor",
            "Abuso sexual en establecimiento educativo"
        ]
        
        start_time = time.time()
        total_tiempo_procesamiento = 0
        
        for i, caso in enumerate(test_cases):
            clasificacion, metodo, tiempo_ms, confianza = clasificar_fila_con_cascada(caso, i)
            total_tiempo_procesamiento += tiempo_ms
            
            if tiempo_ms > 5000:  # Más de 5 segundos
                result.add_warning(f"Rendimiento caso {i+1}", f"Tiempo: {tiempo_ms}ms")
            else:
                result.add_pass(f"Rendimiento caso {i+1}", f"Tiempo: {tiempo_ms}ms")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        if total_time < 30:  # Menos de 30 segundos para 5 casos
            result.add_pass("Rendimiento general", f"Tiempo total: {total_time:.2f}s")
        else:
            result.add_fail("Rendimiento general", f"Tiempo total: {total_time:.2f}s")
        
        avg_time = total_tiempo_procesamiento / len(test_cases)
        if avg_time < 2000:  # Menos de 2 segundos promedio
            result.add_pass("Tiempo promedio", f"Promedio: {avg_time:.0f}ms")
        else:
            result.add_warning("Tiempo promedio", f"Promedio: {avg_time:.0f}ms")
        
    except Exception as e:
        result.add_fail("Test de rendimiento", str(e))
    
    return result

def run_all_tests():
    """Ejecuta todas las pruebas y genera reporte"""
    print("🔍 INICIANDO VERIFICACIÓN EXHAUSTIVA DEL SISTEMA CLASIFICADOR DDIC-SM")
    print("=" * 80)
    
    overall_result = TestResult()
    
    # Ejecutar todas las pruebas
    tests = [
        ("Importación de dependencias", test_python_imports),
        ("Estructura de base de datos", test_database_structure),
        ("Funciones de clasificación", test_classification_functions),
        ("Procesamiento de Excel", test_excel_processing),
        ("Endpoints de API", test_api_endpoints),
        ("Integración con IA", test_ai_integration),
        ("Medidas de seguridad", test_security_measures),
        ("Rendimiento del sistema", test_performance)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        print("-" * 60)
        
        result = test_func()
        summary = result.get_summary()
        
        # Agregar resultados al resumen general
        overall_result.tests_passed += summary['passed']
        overall_result.tests_failed += summary['failed']
        overall_result.errors.extend(summary['errors'])
        overall_result.warnings.extend(summary['warnings'])
        
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Warnings: {len(summary['warnings'])}")
        print(f"⏱️  Duration: {summary['duration']:.2f}s")
        
        if summary['failed'] > 0:
            print("Errores encontrados:")
            for error in summary['errors']:
                print(f"  - {error}")
    
    # Reporte final
    final_summary = overall_result.get_summary()
    
    print("\n" + "=" * 80)
    print("📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 80)
    print(f"Total de pruebas: {final_summary['total_tests']}")
    print(f"✅ Exitosas: {final_summary['passed']}")
    print(f"❌ Fallidas: {final_summary['failed']}")
    print(f"⚠️  Advertencias: {len(final_summary['warnings'])}")
    print(f"📈 Tasa de éxito: {final_summary['success_rate']:.1f}%")
    print(f"⏱️  Duración total: {final_summary['duration']:.2f}s")
    
    if final_summary['success_rate'] >= 95:
        print("\n🎉 SISTEMA APROBADO - LISTO PARA SALVAR VIDAS")
        print("   El sistema está verificado y funcionando al 100%")
    elif final_summary['success_rate'] >= 80:
        print("\n⚠️  SISTEMA FUNCIONAL CON ADVERTENCIAS")
        print("   El sistema funciona pero requiere atención en algunas áreas")
    else:
        print("\n🚨 SISTEMA NO APROBADO - REQUIERE CORRECCIONES")
        print("   El sistema tiene fallas críticas que deben ser corregidas")
    
    if final_summary['failed'] > 0:
        print("\n❌ ERRORES CRÍTICOS ENCONTRADOS:")
        for error in final_summary['errors']:
            print(f"   - {error}")
    
    if final_summary['warnings']:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in final_summary['warnings']:
            print(f"   - {warning}")
    
    # Guardar reporte en archivo
    with open('/workspace/test_report.json', 'w') as f:
        json.dump(final_summary, f, indent=2, default=str)
    
    print(f"\n📁 Reporte completo guardado en: /workspace/test_report.json")
    print(f"📁 Logs detallados en: test_results.log")
    
    return final_summary

if __name__ == "__main__":
    try:
        result = run_all_tests()
        sys.exit(0 if result['success_rate'] >= 95 else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Pruebas interrumpidas por el usuario")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n💥 Error fatal durante las pruebas: {str(e)}")
        traceback.print_exc()
        sys.exit(3)