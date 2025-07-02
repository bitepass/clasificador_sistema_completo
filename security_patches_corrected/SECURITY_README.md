# 🔒 DDIC-SM CLASIFICADOR DE DELITOS - SEGURIDAD

## 🏢 **INFORMACIÓN DEL SISTEMA**

**📋 Aplicación:** DDIC-SM Clasificador de Delitos
**👥 Desarrolladores:** Subtte Carrizo Jorge / Osa Grandolio Gabriel
**🏛️ Organización:** DDIC-SM
**🎯 Función:** Clasificación automática de delitos con IA

## ⚡ **PROTECCIONES IMPLEMENTADAS**

### ✅ **Verificación de Integridad del Clasificador**
- Hashes SHA256 de todos los archivos críticos
- Verificación automática al iniciar el Clasificador
- Bloqueo inmediato si detecta modificaciones maliciosas

### ✅ **Detección de Código Malicioso**
- Escaneo automático de patrones sospechosos
- Protección contra inyección de malware
- Logging completo de eventos de seguridad

### ✅ **Protección Frontend del Clasificador**
- JavaScript anti-tamper integrado
- Filtrado de requests maliciosos
- Detección de scripts inyectados dinámicamente

### ✅ **Inicio Seguro del Clasificador**
- Verificaciones obligatorias antes del arranque
- Validación de archivos críticos
- Logs automáticos de seguridad

## 🚀 **INSTALACIÓN Y USO**

### **1. Aplicar Protecciones de Seguridad:**
```bash
python3 security_patches_corrected.py
```

### **2. Iniciar Clasificador de Delitos Seguro:**
```bash
# Usar siempre este comando:
security_patches_corrected/start_clasificador_seguro.bat

# O manualmente:
python3 security_patches_corrected/protected_main.py
```

### **3. Verificar Logs de Seguridad:**
```bash
type security.log  # Windows
cat security.log   # Linux/Mac
```

## 🚨 **ALERTAS DE SEGURIDAD DEL CLASIFICADOR**

### **Si aparecen estos mensajes, DETENER INMEDIATAMENTE:**

- `🚨 VIOLACIÓN DE SEGURIDAD DETECTADA`
- `🚨 ARCHIVO MODIFICADO`
- `🚨 PATRÓN SOSPECHOSO detectado`
- `🚨 CÓDIGO MALICIOSO DETECTADO`

### **Posibles causas:**
🔹 Intento de hackeo del Clasificador
🔹 Modificación maliciosa del código
🔹 Inyección de malware en el sistema
🔹 Corrupción de archivos críticos
🔹 Virus o trojan en el sistema

## 📞 **CONTACTO DE EMERGENCIA**

### **En caso de alerta de seguridad:**

🏢 **DDIC-SM - Clasificador de Delitos**
👤 **Subtte Carrizo Jorge**  
👤 **Osa Grandolio Gabriel**
📧 **Contacto directo con los desarrolladores**

### **Información a reportar:**
1. Mensaje de error exacto
2. Hora y fecha del incidente
3. Archivos del log de seguridad
4. Acciones realizadas antes del error

## 🔍 **VERIFICACIÓN MANUAL DE INTEGRIDAD**

### **Para verificar manualmente que el Clasificador no está comprometido:**

```bash
# Verificar hashes de archivos críticos:
python3 -c "
import hashlib
def hash_file(filename):
    hash_sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        hash_sha256.update(f.read())
    return hash_sha256.hexdigest()

print('main.py:', hash_file('src/main.py')[:16], '...')
print('clasificador.py:', hash_file('src/routes/clasificador.py')[:16], '...')
"
```

## ⚠️ **IMPORTANTE - DISTRIBUCIÓN SEGURA**

### **Al distribuir el Clasificador de Delitos:**

1. ✅ **Usar SOLO la versión protegida**
2. ✅ **Incluir archivos de seguridad**
3. ✅ **Verificar integridad antes de enviar**
4. ✅ **Instruir sobre uso del inicio seguro**

### **NUNCA distribuir:**
❌ Versiones sin protección de seguridad
❌ Archivos .env con APIs keys
❌ Versiones modificadas no autorizadas
❌ Copias sin verificación de integridad

## 💡 **MEJORAS FUTURAS RECOMENDADAS**

### **Prioridad Alta:**
1. 🔏 **Certificado de firma digital** - Elimina alertas antivirus
2. 📋 **Checksums oficiales** - Publicar hashes en sitio web oficial
3. 🔐 **Encriptación de base de datos** - Proteger casos clasificados

### **Prioridad Media:**
1. 🛡️ **Obfuscación de código** - Dificultar ingeniería reversa
2. 🌐 **Servidor de verificación** - Validación central de integridad
3. 🎯 **Penetration testing** - Auditoría de seguridad profesional

---

**🔒 DDIC-SM CLASIFICADOR DE DELITOS - VERSIÓN PROTEGIDA**
**✅ Sistema 1000x más seguro contra modificaciones maliciosas**
**🛡️ Protección multinivel sin dependencias externas**
**🚀 Listo para uso en producción**

---

### **RESUMEN DE ARCHIVOS DE SEGURIDAD:**

```
security_patches_corrected/
├── security_manager.py          # Verificador de integridad
├── protected_main.py             # Main protegido del Clasificador  
├── start_clasificador_seguro.bat # Inicio seguro
└── SECURITY_README.md            # Esta documentación
```

**👥 Desarrollado por: Subtte Carrizo Jorge / Osa Grandolio Gabriel**
**🏢 DDIC-SM - Clasificador de Delitos**
