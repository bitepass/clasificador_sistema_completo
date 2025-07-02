@echo off
title DDIC-SM CLASIFICADOR DE DELITOS - Inicio Seguro
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                🔒 DDIC-SM                                ║
echo ║            CLASIFICADOR DE DELITOS                      ║
echo ║                 Versión Segura                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 👥 Desarrolladores: Subtte Carrizo Jorge / Osa Grandolio Gabriel
echo 🛡️ Iniciando con verificaciones de seguridad...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 📦 El Clasificador requiere Python 3.8+ para funcionar
    echo 💡 Descargue Python desde: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar archivos críticos del Clasificador
if not exist "security_patches_corrected\security_manager.py" (
    echo ❌ Security Manager del Clasificador no encontrado
    echo 🔒 El sistema puede estar comprometido
    echo 📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel
    echo.
    pause
    exit /b 1
)

if not exist "clasificador-delitos-produccion\build\app\src\main.py" (
    echo ❌ Archivo principal del Clasificador no encontrado
    echo 🔒 Instalación incompleta o comprometida
    echo 📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel
    echo.
    pause
    exit /b 1
)

echo ✅ Archivos del Clasificador verificados
echo.

REM Ejecutar Clasificador protegido
echo 🚀 Iniciando CLASIFICADOR DE DELITOS con protecciones...
echo 🔒 Verificando integridad del sistema...
echo.

python security_patches_corrected\protected_main.py

REM Si llega aquí, hubo un error
echo.
echo ❌ Error en la ejecución del Clasificador
echo 📋 Revisar archivo: security.log
echo 📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel
echo.
pause
