#!/usr/bin/env python3
"""
🔒 DDIC-SM Protected Main - Verificación de Seguridad Automática
ESTE ARCHIVO PROTEGE EL SISTEMA CONTRA MODIFICACIONES MALICIOSAS
"""
import sys
import os
from pathlib import Path

# Agregar directorio de seguridad al path
sys.path.insert(0, str(Path(__file__).parent / "security_patches"))

try:
    # VERIFICACIÓN DE SEGURIDAD OBLIGATORIA
    from security_manager import verify_system_integrity
    
    print("🔒 DDIC-SM - Verificando seguridad del sistema...")
    verify_system_integrity()
    print("✅ Sistema verificado - iniciando aplicación")
    
except ImportError:
    print("🚨 ERROR: Security Manager no encontrado")
    print("🔒 Sistema bloqueado por seguridad")
    sys.exit(1)
except Exception as e:
    print(f"🚨 ERROR DE SEGURIDAD: {e}")
    print("🔒 Sistema bloqueado por seguridad") 
    sys.exit(1)

# Solo después de verificación exitosa, importar main original
try:
    # Cambiar al directorio de la aplicación
    app_dir = Path(__file__).parent / "clasificador-delitos-produccion/build/app/src"
    if app_dir.exists():
        os.chdir(app_dir)
        sys.path.insert(0, str(app_dir))
    
    # Importar y ejecutar main original
    import main
    
    if hasattr(main, 'app'):
        print("🚀 Iniciando servidor Flask protegido...")
        main.app.run(host='0.0.0.0', port=5000, debug=False)  # DEBUG OFF
    else:
        print("❌ No se encontró app Flask en main.py")
        
except ImportError as e:
    print(f"❌ Error importando main.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error ejecutando aplicación: {e}")
    sys.exit(1)
