#!/usr/bin/env python3
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
        """Verifica integridad de archivos críticos"""
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
            self.log_security_event("INTEGRITY_CHECK", "Verificación exitosa - archivos íntegros")
    
    def handle_security_violations(self, violations):
        """Maneja violaciones de seguridad detectadas"""
        print("🚨" * 20)
        print("🔒 VIOLACIÓN DE SEGURIDAD DETECTADA")
        print("🚨" * 20)
        
        for violation in violations:
            print(f"❌ {violation}")
        
        print("\n🔒 ACCIONES TOMADAS:")
        print("✅ Evento registrado en log de seguridad")
        print("✅ Ejecución bloqueada por protección")
        print("\n📞 CONTACTAR INMEDIATAMENTE:")
        print("🏢 DDIC-SM - Subtte Carrizo Jorge / Osa Grandolio Gabriel")
        print("📧 seguridad@ddic-sm.gov.ar")
        
        # Bloquear ejecución
        print("\n🛑 Sistema bloqueado por seguridad")
        sys.exit(1)
    
    def log_security_event(self, event_type, message):
        """Registra eventos de seguridad"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_type}: {message}\n"
        
        try:
            with open(self.security_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Error escribiendo log: {e}")
    
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
                            violation = f"PATRÓN SOSPECHOSO '{pattern}' en {file_path}"
                            self.log_security_event("SUSPICIOUS_CODE", violation)
                            self.handle_security_violations([violation])
                            
                except Exception as e:
                    self.log_security_event("SCAN_ERROR", f"Error escaneando {file_path}: {e}")

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
