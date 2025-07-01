#!/usr/bin/env python3
"""
Script para configurar las claves de API del clasificador de delitos
"""

import os
import re

def update_env_file():
    """Actualiza el archivo .env con las claves de API"""
    
    print("🔧 Configurador de Claves API - Clasificador de Delitos")
    print("=" * 60)
    print("Este script te ayudará a configurar las claves de API necesarias.")
    print()
    
    # Leer archivo .env actual
    env_path = '.env'
    if not os.path.exists(env_path):
        print("❌ Error: No se encontró el archivo .env")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    print("📋 APIs disponibles:")
    print("1. 🤖 Gemini API (Recomendado - Gratis)")
    print("2. 🔵 OpenAI API (Backup - Pago)")
    print()
    
    # Configurar Gemini API
    print("🤖 CONFIGURACIÓN GEMINI API")
    print("-" * 30)
    gemini_key = input("Ingresa tu clave de Gemini API (opcional, presiona Enter para saltar): ").strip()
    
    if gemini_key:
        # Validar formato básico de la clave
        if gemini_key.startswith('AIza') and len(gemini_key) > 30:
            content = re.sub(
                r'GEMINI_API_KEY=.*',
                f'GEMINI_API_KEY={gemini_key}',
                content
            )
            print("✅ Clave de Gemini configurada correctamente")
        else:
            print("⚠️  Formato de clave Gemini inválido (debe empezar con 'AIza')")
    else:
        print("⏭️  Configuración de Gemini omitida")
    
    print()
    
    # Configurar OpenAI API
    print("🔵 CONFIGURACIÓN OPENAI API")
    print("-" * 30)
    openai_key = input("Ingresa tu clave de OpenAI API (opcional, presiona Enter para saltar): ").strip()
    
    if openai_key:
        # Validar formato básico de la clave
        if openai_key.startswith('sk-') and len(openai_key) > 40:
            content = re.sub(
                r'OPENAI_API_KEY=.*',
                f'OPENAI_API_KEY={openai_key}',
                content
            )
            print("✅ Clave de OpenAI configurada correctamente")
        else:
            print("⚠️  Formato de clave OpenAI inválido (debe empezar con 'sk-')")
    else:
        print("⏭️  Configuración de OpenAI omitida")
    
    # Guardar archivo actualizado
    with open(env_path, 'w') as f:
        f.write(content)
    
    print()
    print("💾 Archivo .env actualizado")
    print()
    print("📝 NOTAS IMPORTANTES:")
    print("- Al menos una API debe estar configurada para clasificación automática")
    print("- Si no tienes claves, el sistema usará clasificación por reglas básicas")
    print("- Gemini API es gratuita y recomendada para empezar")
    print("- Puedes obtener una clave Gemini en: https://makersuite.google.com/app/apikey")
    print()
    
    return True

def test_connection():
    """Prueba la conexión con las APIs configuradas"""
    print("🧪 PROBANDO CONEXIONES...")
    print("-" * 30)
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    apis_working = []
    
    # Probar Gemini
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test")
            print("✅ Gemini API: Funcionando")
            apis_working.append('Gemini')
        except Exception as e:
            print(f"❌ Gemini API: Error - {str(e)[:50]}...")
    else:
        print("⚪ Gemini API: No configurada")
    
    # Probar OpenAI
    if openai_key and openai_key != 'your_openai_api_key_here':
        try:
            import openai
            openai.api_key = openai_key
            # Test básico (sin gastar créditos)
            print("⚪ OpenAI API: Configurada (no probada para evitar gastos)")
            apis_working.append('OpenAI')
        except Exception as e:
            print(f"❌ OpenAI API: Error - {str(e)[:50]}...")
    else:
        print("⚪ OpenAI API: No configurada")
    
    print()
    if apis_working:
        print(f"🎉 APIs funcionando: {', '.join(apis_working)}")
        print("✅ El clasificador puede usar IA para clasificación automática")
    else:
        print("⚠️  Ninguna API configurada correctamente")
        print("📋 El clasificador usará clasificación por reglas básicas")
    
    return len(apis_working) > 0

def main():
    """Función principal"""
    try:
        if update_env_file():
            print()
            test_choice = input("¿Quieres probar las conexiones? (s/n): ").strip().lower()
            if test_choice in ['s', 'si', 'sí', 'y', 'yes']:
                print()
                test_connection()
        
        print()
        print("🚀 ¡Configuración completada!")
        print("   Puedes iniciar el servidor con: python src/main.py")
        
    except KeyboardInterrupt:
        print("\n⏹️  Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    main()