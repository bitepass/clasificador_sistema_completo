# Clasificador AI de Documentos

Sistema inteligente para la clasificación automática de documentos criminales.

---

## 🚀 Instalación y ejecución

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/bitepass/clasificador_sistema_completo.git
   cd clasificador-frontend
   ```

2. **Instala las dependencias:**
   ```bash
   npm install
   # o
   pnpm install
   ```

3. **Ejecuta la aplicación:**
   ```bash
   npm run dev
   # o
   pnpm dev
   ```

4. **Abre en tu navegador:**
   - [http://localhost:5173](http://localhost:5173) (o el puerto que indique la terminal)

---

## 🧩 Estructura del proyecto

- `src/App.jsx` — Componente principal, rutas y lógica de la app.
- `src/AppContext.jsx` — Estado global con Context API.
- `src/components/ui/` — Componentes reutilizables (menú, spinner, gráficos, etc).

---

## 🛡️ Seguridad y buenas prácticas

- **Nunca subas tus claves API a GitHub.** Usa archivos `.env` y agrégalos a `.gitignore`.
- El backend espera la clave de Gemini en `GEMINI_API_KEY` dentro de `.env`.
- Si subiste una clave por error, desactívala y genera una nueva.

---

## 🧑‍💻 Uso básico

1. Sube un archivo Excel (.xlsx, .xls) con relatos a clasificar.
2. Espera el procesamiento (verás el progreso y un spinner).
3. Visualiza los resultados, filtra por categoría o busca por texto.
4. Descarga los resultados en Excel.
5. Consulta el gráfico de delitos por categoría.

---

## ♿ Accesibilidad

- Navegación por teclado y soporte para lectores de pantalla.
- Filtros y resultados accesibles.

---

## 📈 Visualización

- Gráfico de barras con cantidad de delitos por categoría.
- Filtros y búsqueda en los resultados.

---

## 📄 Licencia

MIT 