#!/usr/bin/env python3
"""
🔒 DDIC-SM CLASIFICADOR DE DELITOS - Main Protegido
ESTE ARCHIVO PROTEGE EL CLASIFICADOR CONTRA MODIFICACIONES MALICIOSAS

Desarrolladores: Subtte Carrizo Jorge / Osa Grandolio Gabriel
Organización: DDIC-SM
Sistema: Clasificador de Delitos con IA
"""
import sys
import os
from pathlib import Path

print("╔══════════════════════════════════════════════════════════╗")
print("║                🔒 DDIC-SM                                ║")
print("║            CLASIFICADOR DE DELITOS                      ║")
print("║              Verificación de Seguridad                  ║")
print("╚══════════════════════════════════════════════════════════╝")
print()
print("👥 Desarrolladores: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
print()

# Agregar directorio de seguridad al path
security_dir = Path(__file__).parent
sys.path.insert(0, str(security_dir))

try:
    # VERIFICACIÓN DE SEGURIDAD OBLIGATORIA DEL CLASIFICADOR
    from security_manager import verify_clasificador_integrity
    
    print("🔒 Verificando integridad del Clasificador de Delitos...")
    verify_clasificador_integrity()
    print("✅ Clasificador verificado - sistema íntegro")
    print("🚀 Iniciando Clasificador de Delitos...")
    print()
    
except ImportError:
    print("🚨 ERROR CRÍTICO: Security Manager del Clasificador no encontrado")
    print("🔒 El Clasificador está bloqueado por seguridad")
    print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
    sys.exit(1)
except Exception as e:
    print(f"🚨 ERROR DE SEGURIDAD EN CLASIFICADOR: {e}")
    print("🔒 El Clasificador está bloqueado por seguridad")
    print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
    sys.exit(1)

# Solo después de verificación exitosa, iniciar el Clasificador
try:
    # Cambiar al directorio del Clasificador
    clasificador_dir = Path(__file__).parent.parent / "clasificador-delitos-produccion/build/app/src"
    if clasificador_dir.exists():
        os.chdir(clasificador_dir)
        sys.path.insert(0, str(clasificador_dir))
        print(f"📂 Directorio del Clasificador: {clasificador_dir}")
    else:
        print("❌ Directorio del Clasificador no encontrado")
        print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
        sys.exit(1)
    
    # Importar y ejecutar el Clasificador principal
    print("📥 Importando módulo principal del Clasificador...")
    import main
    
    if hasattr(main, 'app'):
        print("🌐 Iniciando servidor Flask del Clasificador...")
        print("🔗 Acceder en: http://localhost:5000")
        print("🛡️ Modo seguro: DEBUG=False")
        print()
        print("✅ DDIC-SM CLASIFICADOR DE DELITOS INICIADO CON PROTECCIONES")
        print("=" * 60)
        
        # Ejecutar Clasificador en modo seguro (sin debug)
        main.app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ No se encontró aplicación Flask en el Clasificador")
        print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
        
except ImportError as e:
    print(f"❌ Error importando Clasificador principal: {e}")
    print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error ejecutando Clasificador de Delitos: {e}")
    print("📞 Contactar: Subtte Carrizo Jorge / Osa Grandolio Gabriel")
    sys.exit(1)
