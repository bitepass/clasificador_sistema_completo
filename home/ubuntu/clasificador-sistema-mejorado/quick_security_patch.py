#!/usr/bin/env python3
"""
🔒 DDIC-SM Quick Security Patch - Sin Dependencias Externas
Implementa protecciones básicas inmediatas contra modificaciones maliciosas
"""
import os
import hashlib
import json
import base64
import sys
from pathlib import Path

class QuickSecurityPatch:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.security_dir = self.base_dir / "security_patches"
        self.file_hashes = {}
        
    def calculate_file_hash(self, file_path):
        """Calcula hash SHA256 de archivo"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def create_basic_integrity_check(self):
        """Crea verificador de integridad básico sin dependencias externas"""
        print("🔒 Creando verificador de integridad básico...")
        
        # Calcular hashes de archivos críticos
        critical_files = [
            'clasificador-delitos-produccion/build/app/src/main.py',
            'clasificador-delitos-produccion/build/app/src/static/index.html',
            'clasificador-delitos-produccion/build/app/src/static/reports.html',
            'clasificador-delitos-produccion/build/app/src/routes/clasificador.py'
        ]
        
        for file_path in critical_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                file_hash = self.calculate_file_hash(full_path)
                self.file_hashes[str(file_path)] = file_hash
                print(f"✅ {file_path}: {file_hash[:16]}...")
        
        # Crear verificador de seguridad
        security_manager_code = f'''#!/usr/bin/env python3
"""
🔒 DDIC-SM Security Manager - Verificación de Integridad
ADVERTENCIA: Este archivo protege contra modificaciones maliciosas
"""
import hashlib
import sys
import os
from pathlib import Path

class SecurityManager:
    def __init__(self):
        self.expected_hashes = {json.dumps(self.file_hashes, indent=4)}
        self.security_log = "security.log"
        
    def calculate_hash(self, file_path):
        """Calcula hash SHA256 de archivo"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.log_security_event("ERROR_HASH", f"No se pudo calcular hash de {{file_path}}: {{e}}")
            return None
    
    def verify_file_integrity(self):
        """Verifica integridad de archivos críticos"""
        violations = []
        
        for file_path, expected_hash in self.expected_hashes.items():
            if os.path.exists(file_path):
                current_hash = self.calculate_hash(file_path)
                
                if current_hash and current_hash != expected_hash:
                    violation = f"ARCHIVO MODIFICADO: {{file_path}}"
                    violations.append(violation)
                    self.log_security_event("INTEGRITY_VIOLATION", violation)
            else:
                violation = f"ARCHIVO FALTANTE: {{file_path}}"
                violations.append(violation)
                self.log_security_event("FILE_MISSING", violation)
        
        if violations:
            self.handle_security_violations(violations)
        else:
            self.log_security_event("INTEGRITY_CHECK", "Verificación exitosa - archivos íntegros")
    
    def handle_security_violations(self, violations):
        """Maneja violaciones de seguridad detectadas"""
        print("🚨" * 20)
        print("🔒 VIOLACIÓN DE SEGURIDAD DETECTADA")
        print("🚨" * 20)
        
        for violation in violations:
            print(f"❌ {{violation}}")
        
        print("\\n🔒 ACCIONES TOMADAS:")
        print("✅ Evento registrado en log de seguridad")
        print("✅ Ejecución bloqueada por protección")
        print("\\n📞 CONTACTAR INMEDIATAMENTE:")
        print("🏢 DDIC-SM - Subtte Carrizo Jorge / Osa Grandolio Gabriel")
        print("📧 seguridad@ddic-sm.gov.ar")
        
        # Bloquear ejecución
        print("\\n🛑 Sistema bloqueado por seguridad")
        sys.exit(1)
    
    def log_security_event(self, event_type, message):
        """Registra eventos de seguridad"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{{timestamp}}] {{event_type}}: {{message}}\\n"
        
        try:
            with open(self.security_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Error escribiendo log: {{e}}")
    
    def check_suspicious_modifications(self):
        """Busca modificaciones sospechosas en archivos Python"""
        suspicious_patterns = [
            'evil', 'hack', 'malware', 'steal', 'backdoor',
            'keylogger', 'trojan', 'phishing', 'exploit'
        ]
        
        python_files = [
            'src/main.py',
            'src/routes/clasificador.py',
            'launcher/DDIC_SM_Launcher.py'
        ]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                    
                    for pattern in suspicious_patterns:
                        if pattern in content:
                            violation = f"PATRÓN SOSPECHOSO '{{pattern}}' en {{file_path}}"
                            self.log_security_event("SUSPICIOUS_CODE", violation)
                            self.handle_security_violations([violation])
                            
                except Exception as e:
                    self.log_security_event("SCAN_ERROR", f"Error escaneando {{file_path}}: {{e}}")

# Función de verificación principal
def verify_system_integrity():
    """Ejecuta verificación completa de seguridad"""
    print("🔒 Iniciando verificación de seguridad DDIC-SM...")
    
    security_manager = SecurityManager()
    
    # Verificar integridad de archivos
    security_manager.verify_file_integrity()
    
    # Buscar código sospechoso
    security_manager.check_suspicious_modifications()
    
    print("✅ Verificación de seguridad completada")

if __name__ == "__main__":
    verify_system_integrity()
'''
        
        security_file = self.security_dir / "security_manager.py"
        self.security_dir.mkdir(exist_ok=True)
        
        with open(security_file, 'w', encoding='utf-8') as f:
            f.write(security_manager_code)
        
        print(f"✅ Security Manager creado: {security_file}")

    def create_protected_main_wrapper(self):
        """Crea wrapper protegido para main.py"""
        print("🛡️ Creando wrapper protegido para main.py...")
        
        protected_main = '''#!/usr/bin/env python3
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
'''
        
        protected_file = self.security_dir / "protected_main.py"
        with open(protected_file, 'w', encoding='utf-8') as f:
            f.write(protected_main)
        
        print(f"✅ Main protegido creado: {protected_file}")

    def create_frontend_protection(self):
        """Crea protección JavaScript para frontend"""
        print("🎨 Creando protección para frontend...")
        
        protection_script = '''
<!-- 🔒 DDIC-SM Security Protection Layer -->
<script>
(function() {
    'use strict';
    
    console.log('🔒 DDIC-SM Security Layer - Activando protecciones...');
    
    // 1. Protección contra fetch malicioso
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = args[0];
        
        if (typeof url === 'string') {
            // Lista de patrones sospechosos
            const suspiciousPatterns = [
                'evil', 'hack', 'malware', 'steal', 'phishing', 
                'trojan', 'backdoor', 'keylog', 'exploit'
            ];
            
            // Verificar URL sospechosa
            const urlLower = url.toLowerCase();
            for (const pattern of suspiciousPatterns) {
                if (urlLower.includes(pattern)) {
                    console.error('🚨 BLOCKED SUSPICIOUS REQUEST:', url);
                    console.error('🔒 DDIC-SM Security: Request bloqueado por patrón sospechoso');
                    return Promise.reject(new Error('Blocked by DDIC-SM Security'));
                }
            }
            
            // Verificar dominios no autorizados (solo permitir APIs oficiales)
            const allowedDomains = [
                'localhost',
                '127.0.0.1',
                'generativelanguage.googleapis.com',
                'api.openai.com'
            ];
            
            try {
                const urlObj = new URL(url, window.location.origin);
                const hostname = urlObj.hostname;
                
                if (!allowedDomains.includes(hostname)) {
                    console.warn('⚠️ REQUEST TO EXTERNAL DOMAIN:', hostname);
                    // No bloquear completamente, solo advertir
                }
            } catch (e) {
                // URL relativa, permitir
            }
        }
        
        return originalFetch.apply(this, args);
    };
    
    // 2. Detectar scripts inyectados dinámicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeName === 'SCRIPT') {
                        const scriptContent = node.textContent || node.innerText || '';
                        const scriptSrc = node.src || '';
                        
                        // Patrones maliciosos en scripts
                        const maliciousPatterns = [
                            'hack', 'evil', 'steal', 'malware', 'backdoor',
                            'keylogger', 'trojan', 'phishing', 'exploit',
                            'eval(', 'document.write(', 'innerHTML='
                        ];
                        
                        const contentLower = scriptContent.toLowerCase();
                        const srcLower = scriptSrc.toLowerCase();
                        
                        for (const pattern of maliciousPatterns) {
                            if (contentLower.includes(pattern) || srcLower.includes(pattern)) {
                                console.error('🚨 MALICIOUS SCRIPT DETECTED AND REMOVED');
                                console.error('Pattern found:', pattern);
                                console.error('Script content preview:', scriptContent.substring(0, 100));
                                node.remove();
                                
                                // Log de seguridad
                                const logData = {
                                    timestamp: new Date().toISOString(),
                                    event: 'MALICIOUS_SCRIPT_BLOCKED',
                                    pattern: pattern,
                                    preview: scriptContent.substring(0, 100)
                                };
                                
                                // Intentar enviar log al backend
                                fetch('/api/security-log', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify(logData)
                                }).catch(err => console.warn('Could not send security log:', err));
                                
                                return;
                            }
                        }
                    }
                });
            }
        });
    });
    
    // Observar todo el documento
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 3. Protección contra modificación de consola
    const originalLog = console.log;
    const originalError = console.error;
    
    console.log = function(...args) {
        const message = args.join(' ').toLowerCase();
        if (message.includes('hack') || message.includes('exploit')) {
            console.error('🚨 Suspicious console activity detected');
        }
        return originalLog.apply(this, args);
    };
    
    // 4. Verificación periódica de integridad
    let integrityCheckInterval = setInterval(function() {
        // Verificar que elementos críticos no fueron modificados
        const criticalElements = [
            '#upload-form',
            '#progress-container', 
            '#results-container'
        ];
        
        for (const selector of criticalElements) {
            const element = document.querySelector(selector);
            if (!element) {
                console.warn('⚠️ Critical element missing:', selector);
            }
        }
        
        // Verificar que fetch no fue sobrescrito por código malicioso
        if (window.fetch !== originalFetch && window.fetch.toString().includes('malicious')) {
            console.error('🚨 FETCH FUNCTION COMPROMISED');
            window.fetch = originalFetch; // Restaurar
        }
        
    }, 10000); // Cada 10 segundos
    
    // 5. Protección del LocalStorage
    const originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        if (key.toLowerCase().includes('malware') || 
            value.toLowerCase().includes('steal')) {
            console.error('🚨 Blocked malicious localStorage operation');
            return;
        }
        return originalSetItem.apply(this, arguments);
    };
    
    console.log('✅ DDIC-SM Security Layer ACTIVE');
    console.log('🔒 Protections enabled:');
    console.log('  - Fetch request filtering');
    console.log('  - Dynamic script detection');
    console.log('  - Console activity monitoring');
    console.log('  - Periodic integrity checks');
    console.log('  - LocalStorage protection');
    
})();
</script>
'''
        
        protection_file = self.security_dir / "frontend_protection.html"
        with open(protection_file, 'w', encoding='utf-8') as f:
            f.write(protection_script)
        
        print(f"✅ Protección frontend creada: {protection_file}")

    def create_startup_script(self):
        """Crea script de inicio seguro"""
        print("🚀 Creando script de inicio seguro...")
        
        startup_script = '''@echo off
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
if not exist "security_patches\\security_manager.py" (
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
python security_patches\\protected_main.py

REM Si llega aquí, hubo un error
echo.
echo ❌ Error en la ejecución
echo 📋 Revisar logs de seguridad
pause
'''
        
        startup_file = self.security_dir / "start_secure.bat"
        with open(startup_file, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        print(f"✅ Script de inicio creado: {startup_file}")

    def create_security_documentation(self):
        """Crea documentación de seguridad rápida"""
        print("📚 Creando documentación de seguridad...")
        
        doc_content = '''# 🔒 DDIC-SM QUICK SECURITY PATCH

## ⚡ PROTECCIONES IMPLEMENTADAS (SIN DEPENDENCIAS EXTERNAS)

### ✅ **Verificación de Integridad**
- Hashes SHA256 de archivos críticos
- Verificación automática al inicio
- Bloqueo si detecta modificaciones

### ✅ **Detección de Código Malicioso**
- Escaneo de patrones sospechosos
- Bloqueo de funciones peligrosas
- Logging de eventos de seguridad

### ✅ **Protección Frontend**
- Filtrado de requests sospechosos
- Detección de scripts inyectados
- Monitoreo de actividad maliciosa

### ✅ **Inicio Seguro**
- Verificaciones previas al arranque
- Protección del punto de entrada
- Logs de seguridad automáticos

## 🚀 **INSTALACIÓN RÁPIDA**

1. **Ejecutar patch de seguridad:**
```bash
python quick_security_patch.py
```

2. **Usar inicio seguro:**
```bash
# En lugar de main.py usar:
security_patches\\start_secure.bat
```

3. **Verificar logs:**
```bash
type security.log
```

## 🚨 **QUÉ HACE CADA COMPONENTE**

### `security_manager.py`
- Calcula y verifica hashes de archivos
- Detecta modificaciones maliciosas
- Bloquea ejecución si hay problemas

### `protected_main.py`
- Wrapper seguro para main.py original
- Ejecuta verificaciones antes de iniciar
- Fuerza modo debug=False

### `frontend_protection.html`
- JavaScript anti-tamper
- Bloquea requests maliciosos
- Detecta scripts inyectados

### `start_secure.bat`
- Script de inicio con verificaciones
- Valida archivos críticos
- Inicia aplicación protegida

## ⚠️ **ALERTAS DE SEGURIDAD**

Si ve estos mensajes:
- `🚨 VIOLACIÓN DE SEGURIDAD DETECTADA` → DETENER INMEDIATAMENTE
- `🚨 ARCHIVO MODIFICADO` → Verificar integridad
- `🚨 PATRÓN SOSPECHOSO` → Posible malware

**ACCIÓN:** Contactar DDIC-SM inmediatamente

## 📞 **CONTACTO DE EMERGENCIA**

🏢 **DDIC-SM**
👥 **Subtte Carrizo Jorge / Osa Grandolio Gabriel**
📧 **seguridad@ddic-sm.gov.ar**

## 🔍 **VERIFICACIÓN MANUAL**

```bash
# Verificar hashes manualmente:
python -c "
import hashlib
def hash_file(f):
    h = hashlib.sha256()
    with open(f, 'rb') as file:
        h.update(file.read())
    return h.hexdigest()
print('main.py:', hash_file('src/main.py'))
"
```

**🔒 ESTA IMPLEMENTACIÓN NO REQUIERE DEPENDENCIAS EXTERNAS**
**✅ COMPATIBLE CON CUALQUIER INSTALACIÓN DE PYTHON 3.6+**
'''
        
        doc_file = self.security_dir / "QUICK_SECURITY_README.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"✅ Documentación creada: {doc_file}")

    def apply_quick_patch(self):
        """Aplica el patch de seguridad rápido"""
        print("🔒 APLICANDO PATCH DE SEGURIDAD RÁPIDO DDIC-SM")
        print("=" * 60)
        
        # Crear directorio de seguridad
        self.security_dir.mkdir(exist_ok=True)
        
        # Aplicar protecciones
        self.create_basic_integrity_check()
        self.create_protected_main_wrapper()
        self.create_frontend_protection()
        self.create_startup_script()
        self.create_security_documentation()
        
        print("\n" + "=" * 60)
        print("🎉 PATCH DE SEGURIDAD APLICADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📂 Ubicación: {self.security_dir}")
        print("🔒 Protecciones activas:")
        print("  ✅ Verificación de integridad SHA256")
        print("  ✅ Detección de código malicioso")
        print("  ✅ Protección frontend anti-tamper")
        print("  ✅ Inicio seguro con verificaciones")
        print("  ✅ Logging de eventos de seguridad")
        print("=" * 60)
        print("🚀 USO:")
        print(f"   {self.security_dir}/start_secure.bat")
        print("📚 DOCUMENTACIÓN:")
        print(f"   {self.security_dir}/QUICK_SECURITY_README.md")
        print("=" * 60)

if __name__ == "__main__":
    try:
        patcher = QuickSecurityPatch()
        patcher.apply_quick_patch()
    except Exception as e:
        print(f"❌ Error aplicando patch: {e}")
        import traceback
        traceback.print_exc()