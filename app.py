import os
import json
from flask import Flask, render_template, render_template_string, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
# type: ignore comment for IDEs and remove unused numpy
import pandas as pd

# -----------------------------------
# Configuración general
# -----------------------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

app = Flask(__name__)
app.secret_key = "cambia_esta_clave"  # Cambia esta clave en producción
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Límite de subida (100 MB)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variables globales para almacenar datos y nombre de archivo actual
current_data: pd.DataFrame | None = None
current_filename: str | None = None

# -----------------------------------
# Utilidades
# -----------------------------------

def allowed_file(filename: str) -> bool:
    """Comprobar si la extensión del archivo es válida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_file(filepath: str) -> pd.DataFrame:
    """Cargar un archivo CSV/XLS/XLSX a un DataFrame de pandas."""
    try:
        if filepath.lower().endswith(".csv"):
            # Probar distintos encodings
            encodings = [
                "utf-8",
                "latin1",
                "cp1252",
                "iso-8859-1",
                "utf-16",
            ]
            for enc in encodings:
                try:
                    return pd.read_csv(filepath, encoding=enc)
                except UnicodeDecodeError:
                    continue
            # Si ninguno funcionó
            raise UnicodeDecodeError(
                "", b"", 0, 0, "No se pudo decodificar el CSV con los encodings estándar"
            )
        else:
            # Excel (soporta xls y xlsx)
            return pd.read_excel(filepath)
    except Exception as exc:
        raise RuntimeError(f"Error al leer el archivo: {exc}") from exc


def get_context(df: pd.DataFrame, row_idx: int, max_cols: int = 10) -> dict:
    """Obtener hasta `max_cols` celdas de contexto de la fila indicada."""
    context: dict[str, str] = {}
    for col in df.columns[:max_cols]:
        value = df.at[row_idx, col]
        if pd.notna(value):
            context[str(col)] = str(value)
    return context


def search_in_dataframe(
    df: pd.DataFrame,
    term: str,
    case_sensitive: bool = False,
    selected_columns: list[str] | None = None,
) -> list[dict]:
    """Buscar `term` en las columnas seleccionadas del DataFrame."""
    if not case_sensitive:
        term = term.lower()

    columns_to_search = (
        df.columns if not selected_columns else [c for c in selected_columns if c in df.columns]
    )

    results: list[dict] = []

    for col_idx, column in enumerate(df.columns):
        if column not in columns_to_search:
            continue

        series = df[column]
        for row_idx, value in series.items():
            if pd.isna(value):
                continue
            text = str(value)
            haystack = text if case_sensitive else text.lower()
            if term in haystack:
                results.append(
                    {
                        "fila": row_idx + 2,  # +2: desplazamiento por encabezados (Excel comienza en 1)
                        "columna": str(column),
                        "columna_numero": col_idx + 1,
                        "texto_completo": text,
                        "contexto": get_context(df, row_idx),
                    }
                )
    return results

# -----------------------------------
# Rutas
# -----------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    global current_data, current_filename

    if "file" not in request.files:
        flash("No se seleccionó ningún archivo")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("Nombre de archivo vacío")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        try:
            current_data = load_file(filepath)
            current_filename = filename
            flash(
                f"Archivo '{filename}' cargado correctamente · {len(current_data)} filas · {len(current_data.columns)} columnas"
            )
            # Borrar archivo temporal
            os.remove(filepath)
            return redirect(url_for("search_page"))
        except Exception as exc:
            flash(str(exc))
            return redirect(url_for("index"))

    flash("Tipo de archivo no permitido. Solo CSV, XLS, XLSX")
    return redirect(url_for("index"))


@app.route("/search")
def search_page():
    if current_data is None:
        flash("Primero debe cargar un archivo")
        return redirect(url_for("index"))

    # Garantiza a los analizadores estáticos que current_data no es None
    assert current_data is not None

    return render_template(
        "search.html",
        filename=current_filename,
        columns=list(current_data.columns),
        total_rows=len(current_data),
    )


@app.route("/api/search", methods=["POST"])
def api_search():
    if current_data is None:
        return jsonify({"error": "No hay datos cargados"}), 400

    body = request.get_json(silent=True) or {}
    term = body.get("search_term", "").strip()
    case_sensitive = body.get("case_sensitive", False)
    selected_columns = body.get("selected_columns", [])

    if not term:
        return jsonify({"error": "Debe ingresar un término de búsqueda"}), 400

    try:
        results = search_in_dataframe(current_data, term, case_sensitive, selected_columns)
        return jsonify(
            {
                "results": results,
                "total_results": len(results),
                "search_term": term,
                "searched_columns": selected_columns or list(current_data.columns),
            }
        )
    except Exception as exc:
        return jsonify({"error": f"Error en la búsqueda: {exc}"}), 500


@app.route("/reset")
def reset():
    global current_data, current_filename
    current_data = None
    current_filename = None
    flash("Sesión reiniciada")
    return redirect(url_for("index"))

# -----------------------------------
# Templates embebidos -> se escriben en disco al inicio
# -----------------------------------

INDEX_HTML = """<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Buscador de Texto en Excel/CSV</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)}
        .card{background:rgba(255,255,255,.15);backdrop-filter:blur(20px);padding:40px;border-radius:20px;width:90%;max-width:500px;border:1px solid rgba(255,255,255,.2);box-shadow:0 8px 32px rgba(0,0,0,.1);text-align:center;color:#fff}
        h1{font-weight:300;margin-bottom:30px}
        .upload{border:2px dashed rgba(255,255,255,.4);padding:40px;border-radius:15px;transition:.3s}
        .upload:hover{background:rgba(255,255,255,.1)}
        input[type=file]{margin:20px auto;color:#fff;width:100%}
        input[type=file]::-webkit-file-upload-button{background:rgba(0,0,0,.8);border:none;color:#fff;padding:10px 20px;border-radius:8px;cursor:pointer}
        button{background:rgba(0,0,0,.8);color:#fff;border:none;padding:12px 24px;border-radius:12px;font-size:16px;cursor:pointer;transition:.3s}
        button:hover{background:rgba(0,0,0,.9)}
        .flash{margin-top:20px;background:rgba(255,255,255,.2);padding:15px;border-radius:10px}
    </style>
</head>
<body>
    <div class=\"card\">
        <h1>🔍 Buscador Excel / CSV</h1>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for m in messages %}<div class=\"flash\">{{m}}</div>{% endfor %}
        {% endif %}
        {% endwith %}
        <form action=\"/upload\" method=\"post\" enctype=\"multipart/form-data\">
            <div class=\"upload\">
                <input type=\"file\" name=\"file\" accept=\".csv,.xls,.xlsx\" required>
                <button type=\"submit\">Cargar Archivo</button>
            </div>
        </form>
    </div>
</body>
</html>"""

SEARCH_HTML = """<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Buscar en {{ filename }}</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;min-height:100vh;padding:20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff}
        .container{max-width:1200px;margin:0 auto;background:rgba(255,255,255,.15);backdrop-filter:blur(20px);padding:40px;border-radius:20px;border:1px solid rgba(255,255,255,.2);box-shadow:0 8px 32px rgba(0,0,0,.1)}
        h1{font-weight:300;margin-bottom:25px}
        .file-info{background:rgba(255,255,255,.1);padding:20px;border-radius:15px;margin-bottom:25px}
        .search-box{display:flex;gap:15px;flex-wrap:wrap;margin-bottom:25px}
        .search-box input{flex:1;min-width:200px;padding:15px;border-radius:15px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);color:#fff}
        .search-box button{padding:12px 24px;border:none;border-radius:12px;background:rgba(0,0,0,.8);color:#fff;cursor:pointer;transition:.3s}
        .search-box button:hover{background:rgba(0,0,0,.9)}
        .column-selector{background:rgba(255,255,255,.1);padding:25px;border-radius:15px;margin-bottom:25px}
        .columns-container{display:flex;flex-wrap:wrap;gap:12px}
        .chip{padding:8px 16px;border-radius:20px;background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.3);cursor:pointer;user-select:none;transition:.3s}
        .chip.inactive{background:rgba(0,0,0,.3);opacity:.6}
        .chip:hover{background:rgba(255,255,255,.3)}
        .results-container{margin-top:30px}
        .result{background:rgba(255,255,255,.1);padding:20px;border-radius:15px;margin-bottom:15px;border:1px solid rgba(255,255,255,.2)}
        .context{margin-top:15px;background:rgba(0,0,0,.2);padding:15px;border-radius:10px;font-size:13px}
        .no-results,.loading{text-align:center;padding:40px;font-size:18px}
    </style>
</head>
<body>
<div class=\"container\">
    <h1>🔍 Buscar en: {{ filename }}</h1>

    <div class=\"file-info\">
        <strong>Archivo:</strong> {{ filename }}<br>
        <strong>Filas:</strong> {{ total_rows }}<br>
        <strong>Columnas:</strong> {{ columns|length }}
    </div>

    <div class=\"column-selector\">
        <h4>Selecciona columnas donde buscar:</h4>
        <div class=\"columns-container\" id=\"columnsContainer\">
            {% for column in columns %}
            <div class=\"chip\" onclick=\"toggleColumn('{{ column }}', this)\">{{ column }}</div>
            {% endfor %}
        </div>
    </div>

    <div class=\"search-box\">
        <input id=\"searchInput\" placeholder=\"Buscar texto...\" onkeypress=\"if(event.key==='Enter') search();\">
        <button onclick=\"search()\">Buscar</button>
        <label style=\"display:flex;align-items:center;gap:5px\">
            <input type=\"checkbox\" id=\"caseSensitive\">Mayúsculas
        </label>
        <a href=\"/reset\" style=\"color:#fff;background:rgba(255,255,255,.2);padding:12px 24px;border-radius:12px;text-decoration:none\">Nuevo archivo</a>
    </div>

    <div id=\"results\"></div>
</div>

<script>
    let selectedColumns = [...{{ columns|tojson }}];
    function toggleColumn(name, el){
        const idx = selectedColumns.indexOf(name);
        if(idx>-1){selectedColumns.splice(idx,1);el.classList.add('inactive');}
        else {selectedColumns.push(name);el.classList.remove('inactive');}
    }

    function search(){
        const term = document.getElementById('searchInput').value.trim();
        const cs = document.getElementById('caseSensitive').checked;
        const resultsDiv = document.getElementById('results');
        if(!term){alert('Ingrese un término');return;}
        if(selectedColumns.length===0){alert('Seleccione al menos una columna');return;}
        resultsDiv.innerHTML = '<div class="loading">Buscando...</div>';
        fetch('/api/search',{
            method:'POST',headers:{'Content-Type':'application/json'},
            body:JSON.stringify({search_term:term,case_sensitive:cs,selected_columns:selectedColumns})
        }).then(r=>r.json()).then(data=>{
            if(data.error){resultsDiv.innerHTML='<div class="no-results">'+data.error+'</div>';return;}
            if(data.results.length===0){resultsDiv.innerHTML='<div class="no-results">Sin resultados</div>';return;}
            let html='<div class="results-container">';
            html+='<h3>Encontrados '+data.total_results+' resultados</h3>';
            data.results.forEach((res,i)=>{
                html+='<div class="result">'+
                    '<strong>Resultado '+(i+1)+': Fila '+res.fila+', Columna "'+res.columna+'"</strong><br><br>'+
                    '<div>'+res.texto_completo+'</div>'+
                    '<div class="context"><strong>Contexto:</strong><br>'+Object.entries(res.contexto).map(([k,v])=>k+': '+v).join('<br>')+'</div>'+
                    '</div>';
            });
            html+='</div>';
            resultsDiv.innerHTML = html;
        }).catch(e=>resultsDiv.innerHTML='<div class="no-results">Error: '+e+'</div>');
    }

    document.getElementById('searchInput').focus();
</script>
</body>
</html>"""


# -----------------------------------
# Helper para garantizar que existan templates
# -----------------------------------

def _write_templates() -> None:
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    os.makedirs(templates_dir, exist_ok=True)
    with open(os.path.join(templates_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)
    with open(os.path.join(templates_dir, "search.html"), "w", encoding="utf-8") as f:
        f.write(SEARCH_HTML)


# -----------------------------------
# Punto de entrada
# -----------------------------------

if __name__ == "__main__":
    _write_templates()
    print("🚀 Servidor iniciado → http://localhost:5000")
    print("📋 Soporta archivos: CSV, XLS, XLSX")
    app.run(debug=True, host="0.0.0.0", port=5000)