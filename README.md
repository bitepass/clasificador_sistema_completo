# Buscador de palabras en Excel / CSV 📊🔍

Aplicación web en Python que permite cargar archivos **Excel** (`.xlsx`, `.xls`) o **CSV**, buscar texto en las columnas seleccionadas y mostrar contexto de cada coincidencia. Interfaz moderna con estilo *glassmorphism*.

---

## 🚀 Instalación

1. Clona el repositorio o copia los archivos en tu máquina.

```bash
cd /ruta/al/proyecto
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Ejecuta la aplicación:

```bash
python app.py
```

3. Abre tu navegador en `http://localhost:5000`.

---

## ⚙️ Uso

1. En la página principal, carga un archivo **CSV** o **Excel**.
2. Tras la carga, verás información del archivo y un selector de columnas.
3. Escribe el término a buscar, elige si distingue mayúsculas y haz clic en **Buscar**.
4. Se mostrarán todas las coincidencias con:
   * Fila y columna (número y nombre).
   * Texto completo de la celda.
   * Contexto (otras columnas de la misma fila).
5. Usa el enlace **Nuevo archivo** para reiniciar la sesión y cargar otro archivo.

---

## 📂 Estructura del proyecto

```
├── app.py           # Aplicación Flask (genera templates al vuelo)
├── requirements.txt # Dependencias del proyecto
├── README.md        # Este archivo
└── uploads/         # Carpeta temporal para archivos subidos
```

---

## ✨ Características destacadas

- Detección automática de codificación para CSV.
- Selección dinámica de columnas con "chips" clicables.
- Búsqueda sensible / no sensible a mayúsculas.
- Resultados enriquecidos con contexto.
- Estilo *glassmorphism* responsive.

---

## 🛡️ Notas de seguridad

- Cambia `app.secret_key` por un valor seguro en producción.
- Ajusta `MAX_CONTENT_LENGTH` si necesitas permitir archivos más grandes.