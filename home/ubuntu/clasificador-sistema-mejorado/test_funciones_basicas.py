#!/usr/bin/env python3
"""
🔍 PRUEBA BÁSICA DE FUNCIONES DE CLASIFICACIÓN
==============================================

Test simple para verificar que las funciones críticas funcionan correctamente.
"""

import sys
import os
import time

# Agregar ruta del proyecto
sys.path.insert(0, '/workspace/home/ubuntu/clasificador-sistema-mejorado')

def test_imports():
    """Verificar importaciones críticas"""
    print("🧪 Test 1: Verificando importaciones...")
    
    try:
        from src.routes.clasificador import (
            clasificacion_basada_en_reglas, 
            clasificacion_por_defecto,
            limpiar_clasificacion,
            clasificar_fila_con_cascada,
            CATEGORIAS_CLASIFICACION
        )
        print("✅ PASS: Importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ FAIL: Error en importaciones - {e}")
        return False

def test_classification_functions():
    """Verificar funciones de clasificación"""
    print("\n🧪 Test 2: Verificando funciones de clasificación...")
    
    try:
        from src.routes.clasificador import (
            clasificacion_basada_en_reglas, 
            clasificacion_por_defecto,
            limpiar_clasificacion,
            clasificar_fila_con_cascada
        )
        
        # Test 1: Clasificación por defecto
        clasificacion_def, metodo_def = clasificacion_por_defecto()
        if isinstance(clasificacion_def, dict) and metodo_def == 'DEFECTO':
            print("✅ PASS: Clasificación por defecto funciona")
        else:
            print("❌ FAIL: Clasificación por defecto no funciona")
            return False
        
        # Test 2: Clasificación por reglas
        texto_test = "Robo con arma de fuego en vía pública a una mujer"
        clasificacion_reglas, metodo_reglas = clasificacion_basada_en_reglas(texto_test)
        
        if isinstance(clasificacion_reglas, dict) and metodo_reglas == 'REGLAS':
            print("✅ PASS: Clasificación por reglas funciona")
        else:
            print("❌ FAIL: Clasificación por reglas no funciona")
            return False
        
        # Test 3: Verificar estructura de clasificación
        required_keys = ['JURISDICCION', 'CALIFICACION', 'MODALIDAD', 'VICTIMAS', 'ARMAS', 'LUGAR']
        for key in required_keys:
            if key not in clasificacion_reglas:
                print(f"❌ FAIL: Falta clave {key} en clasificación")
                return False
        print("✅ PASS: Estructura de clasificación correcta")
        
        # Test 4: Limpieza de clasificación
        clasificacion_limpia = limpiar_clasificacion(clasificacion_reglas)
        if isinstance(clasificacion_limpia, dict):
            print("✅ PASS: Limpieza de clasificación funciona")
        else:
            print("❌ FAIL: Limpieza de clasificación no funciona")
            return False
        
        # Test 5: Clasificación con cascada
        clasificacion, metodo, tiempo_ms, confianza = clasificar_fila_con_cascada(texto_test, 1)
        
        if isinstance(clasificacion, dict) and isinstance(tiempo_ms, int) and isinstance(confianza, float):
            print("✅ PASS: Clasificación con cascada funciona")
        else:
            print("❌ FAIL: Clasificación con cascada no funciona")
            return False
        
        # Test 6: Verificar que retorna estructura válida
        if all(key in clasificacion for key in ['JURISDICCION', 'CALIFICACION', 'MODALIDAD']):
            print("✅ PASS: Clasificación con cascada retorna estructura válida")
        else:
            print("❌ FAIL: Clasificación con cascada retorna estructura inválida")
            print(f"Estructura recibida: {list(clasificacion.keys())}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error en funciones de clasificación - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_excel_processing():
    """Verificar procesamiento de Excel"""
    print("\n🧪 Test 3: Verificando procesamiento de Excel...")
    
    try:
        import pandas as pd
        from src.routes.clasificador import clasificar_fila_con_cascada
        
        # Crear datos de prueba
        test_data = {
            'relato': [
                'Robo con arma de fuego en vía pública',
                'Homicidio simple en domicilio particular',
                'Lesiones con arma blanca en comercio'
            ]
        }
        
        df = pd.DataFrame(test_data)
        print("✅ PASS: DataFrame de prueba creado")
        
        # Procesar cada fila
        all_ok = True
        for index, row in df.iterrows():
            clasificacion, metodo, tiempo, confianza = clasificar_fila_con_cascada(row['relato'], index)
            
            if not isinstance(clasificacion, dict) or 'JURISDICCION' not in clasificacion:
                print(f"❌ FAIL: Procesamiento fila {index + 1} - estructura inválida")
                all_ok = False
            else:
                print(f"✅ PASS: Procesamiento fila {index + 1} - OK")
        
        if all_ok:
            print("✅ PASS: Procesamiento de Excel completo")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ FAIL: Error en procesamiento Excel - {e}")
        return False

def test_performance():
    """Verificar rendimiento básico"""
    print("\n🧪 Test 4: Verificando rendimiento...")
    
    try:
        from src.routes.clasificador import clasificar_fila_con_cascada
        
        casos_test = [
            "Robo con arma de fuego",
            "Homicidio simple",
            "Lesiones con arma blanca",
            "Estafa por WhatsApp",
            "Abuso sexual"
        ]
        
        start_time = time.time()
        for i, caso in enumerate(casos_test):
            clasificacion, metodo, tiempo_ms, confianza = clasificar_fila_con_cascada(caso, i)
            
            if tiempo_ms > 1000:  # Más de 1 segundo es demasiado lento para reglas
                print(f"⚠️  WARN: Caso {i+1} lento: {tiempo_ms}ms")
            else:
                print(f"✅ PASS: Caso {i+1} rápido: {tiempo_ms}ms")
        
        total_time = time.time() - start_time
        if total_time < 5:  # Menos de 5 segundos para 5 casos
            print(f"✅ PASS: Rendimiento general: {total_time:.2f}s")
            return True
        else:
            print(f"❌ FAIL: Rendimiento lento: {total_time:.2f}s")
            return False
        
    except Exception as e:
        print(f"❌ FAIL: Error en test de rendimiento - {e}")
        return False

def run_basic_tests():
    """Ejecutar todas las pruebas básicas"""
    print("🔍 INICIANDO PRUEBAS BÁSICAS DEL CLASIFICADOR DDIC-SM")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Funciones de clasificación", test_classification_functions),
        ("Procesamiento Excel", test_excel_processing),
        ("Rendimiento", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: EXITOSO")
        else:
            print(f"❌ {test_name}: FALLIDO")
    
    # Resultado final
    success_rate = (passed / total) * 100
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    print(f"Pruebas exitosas: {passed}/{total}")
    print(f"Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🎉 ¡TODAS LAS FUNCIONES BÁSICAS FUNCIONAN PERFECTAMENTE!")
        print("   El sistema está listo para salvar vidas con datos precisos")
    elif success_rate >= 75:
        print("\n⚠️  Sistema funcional con algunas advertencias")
    else:
        print("\n🚨 Sistema requiere correcciones críticas")
    
    return success_rate >= 100

if __name__ == "__main__":
    try:
        success = run_basic_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)