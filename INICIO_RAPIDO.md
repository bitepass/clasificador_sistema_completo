# 🚀 Guía de Inicio Rápido

## Para empezar AHORA:

### 1. Instalar dependencias
```bash
python instalar.py
```

### 2. Ejecutar programa
```bash
python app.py
```

### 3. Abrir navegador
Ve a: `http://localhost:5000`

### 4. Probar con datos de ejemplo
- Usa el archivo `ejemplo_datos.csv` incluido
- Busca palabras como: "Madrid", "Desarrollador", "TechCorp"

---

## 🎯 Casos de prueba sugeridos:

### Búsqueda básica:
- **Palabra**: "Madrid"
- **Resultado**: Aparece en la columna "Ciudad"

### Búsqueda por cargo:
- **Palabra**: "Desarrollador"
- **Resultado**: Aparece en la columna "Cargo"

### Búsqueda por empresa:
- **Palabra**: "TechCorp"
- **Resultado**: Aparece en la columna "Empresa"

### Búsqueda numérica:
- **Palabra**: "45000"
- **Resultado**: Aparece en la columna "Salario"

### Búsqueda con filtros:
- **Seleccionar solo**: Columnas "Nombre" y "Apellido"
- **Buscar**: "Juan"
- **Resultado**: Solo buscará en las columnas seleccionadas

---

## 🔧 Ejecución alternativa:

### Opción 1: Script automático
```bash
python ejecutar.py
```

### Opción 2: Directo
```bash
python app.py
```

### Opción 3: Con configuración
```bash
FLASK_ENV=development python app.py
```

---

## 🎨 Funciones destacadas:

✅ **Selector de columnas**: Haz clic en los chips azules  
✅ **Búsqueda sensible**: Marca el checkbox para mayúsculas  
✅ **Contexto completo**: Ve toda la información de cada fila  
✅ **Diseño moderno**: Interfaz glassmorphism  
✅ **Múltiples formatos**: CSV, XLS, XLSX  

---

## 📞 ¿Problemas?

### Error de dependencias:
```bash
pip install --break-system-packages Flask pandas openpyxl xlrd Werkzeug numpy
```

### Puerto ocupado:
- Cierra otros servidores en puerto 5000
- O edita `app.py` y cambia el puerto

### Archivo no se carga:
- Verifica que sea .csv, .xls o .xlsx
- Prueba con `ejemplo_datos.csv`

---

**¡Listo para buscar! 🎉**