#!/usr/bin/env python3
"""
🔒 DDIC-SM CLASIFICADOR DE DELITOS - Security Manager
ADVERTENCIA: Este archivo protege contra modificaciones maliciosas
CONTACTO: Subtte Carrizo Jorge / Osa Grandolio Gabriel
"""
import hashlib
import sys
import os
from pathlib import Path

class SecurityManager:
    def __init__(self):
        self.expected_hashes = {}
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
            self.log_security_event("ERROR_HASH", f"No se pudo calcular hash de {file_path}: {e}")
            return None
    
    def verify_file_integrity(self):
        """Verifica integridad de archivos críticos del Clasificador de Delitos"""
        violations = []
        
        for file_path, expected_hash in self.expected_hashes.items():
            if os.path.exists(file_path):
                current_hash = self.calculate_hash(file_path)
                
                if current_hash and current_hash != expected_hash:
                    violation = f"ARCHIVO MODIFICADO: {file_path}"
                    violations.append(violation)
                    self.log_security_event("INTEGRITY_VIOLATION", violation)
            else:
                violation = f"ARCHIVO FALTANTE: {file_path}"
                violations.append(violation)
                self.log_security_event("FILE_MISSING", violation)
        
        if violations:
            self.handle_security_violations(violations)
        else:
            self.log_security_event("INTEGRITY_CHECK", "Verificación exitosa - Clasificador de Delitos íntegro")
    
    def handle_security_violations(self, violations):
        """Maneja violaciones de seguridad detectadas"""
        print("🚨" * 30)
        print("🔒 VIOLACIÓN DE SEGURIDAD DETECTADA")
        print("📋 DDIC-SM CLASIFICADOR DE DELITOS")
        print("🚨" * 30)
        
        for violation in violations:
            print(f"❌ {violation}")
        
        print("\n🔒 ACCIONES TOMADAS:")
        print("✅ Evento registrado en log de seguridad")
        print("✅ Ejecución del Clasificador bloqueada por protección")
        print("\n📞 CONTACTAR INMEDIATAMENTE:")
        print("🏢 DDIC-SM - Clasificador de Delitos")
        print("👥 Subtte Carrizo Jorge")
        print("👥 Osa Grandolio Gabriel")
        print("📧 Contacto directo con los desarrolladores")
        print("\n⚠️  POSIBLES CAUSAS:")
        print("🔹 Modificación maliciosa del código")
        print("🔹 Intento de hackeo del sistema")
        print("🔹 Corrupción de archivos")
        print("🔹 Inyección de malware")
        
        # Bloquear ejecución del Clasificador
        print("\n🛑 CLASIFICADOR DE DELITOS BLOQUEADO POR SEGURIDAD")
        sys.exit(1)
    
    def log_security_event(self, event_type, message):
        """Registra eventos de seguridad del Clasificador"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] DDIC-SM CLASIFICADOR - {event_type}: {message}\n"
        
        try:
            with open(self.security_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Error escribiendo log de seguridad: {e}")
    
    def check_suspicious_modifications(self):
        """Busca modificaciones sospechosas en archivos del Clasificador"""
        suspicious_patterns = [
            'evil', 'hack', 'malware', 'steal', 'backdoor',
            'keylogger', 'trojan', 'phishing', 'exploit',
            'virus', 'worm', 'rootkit', 'spyware'
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
                            violation = f"PATRÓN SOSPECHOSO '{pattern}' detectado en {file_path}"
                            self.log_security_event("SUSPICIOUS_CODE", violation)
                            print(f"🚨 CÓDIGO MALICIOSO DETECTADO: {pattern} en {file_path}")
                            self.handle_security_violations([violation])
                            
                except Exception as e:
                    self.log_security_event("SCAN_ERROR", f"Error escaneando {file_path}: {e}")

# Función de verificación principal del Clasificador
def verify_clasificador_integrity():
    """Ejecuta verificación completa de seguridad del Clasificador de Delitos"""
    print("🔒 DDIC-SM CLASIFICADOR DE DELITOS")
    print("🛡️ Iniciando verificación de seguridad...")
    
    security_manager = SecurityManager()
    
    # Verificar integridad de archivos del Clasificador
    security_manager.verify_file_integrity()
    
    # Buscar código malicioso en el Clasificador
    security_manager.check_suspicious_modifications()
    
    print("✅ Verificación de seguridad del Clasificador completada")
    print("🚀 Clasificador de Delitos listo para usar")

if __name__ == "__main__":
    verify_clasificador_integrity()
