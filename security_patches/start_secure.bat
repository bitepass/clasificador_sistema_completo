@echo off
title DDIC-SM Clasificador - Inicio Seguro
echo.
echo 🔒 DDIC-SM CLASIFICADOR DE DELITOS
echo ═══════════════════════════════════════
echo.
echo 🛡️ Iniciando con verificaciones de seguridad...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 📦 Instale Python 3.8+ para continuar
    pause
    exit /b 1
)

REM Verificar archivos críticos
if not exist "security_patches\security_manager.py" (
    echo ❌ Security Manager no encontrado
    echo 🔒 Sistema puede estar comprometido
    pause
    exit /b 1
)

if not exist "protected_main.py" (
    echo ❌ Main protegido no encontrado
    echo 🔒 Sistema puede estar comprometido  
    pause
    exit /b 1
)

echo ✅ Archivos de seguridad verificados
echo.

REM Ejecutar aplicación protegida
echo 🚀 Iniciando aplicación con protecciones...
python security_patches\protected_main.py

REM Si llega aquí, hubo un error
echo.
echo ❌ Error en la ejecución
echo 📋 Revisar logs de seguridad
pause
