from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración para subida de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variable global para almacenar los datos
current_data = None
current_filename = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_file(filepath):
    """Cargar archivo Excel o CSV"""
    try:
        if filepath.endswith('.csv'):
            # Intentar diferentes encodings para CSV
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    return df
                except UnicodeDecodeError:
                    continue
            raise Exception("No se pudo leer el archivo CSV con ninguna codificación")
        else:
            # Para archivos Excel
            df = pd.read_excel(filepath)
            return df
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {str(e)}")

def search_in_dataframe(df, search_term, case_sensitive=False, selected_columns=None):
    """Buscar término en columnas específicas del DataFrame"""
    results = []
    
    # Convertir término de búsqueda
    if not case_sensitive:
        search_term = search_term.lower()
    
    # Si no se especifican columnas, usar todas
    if selected_columns is None or len(selected_columns) == 0:
        columns_to_search = df.columns
    else:
        columns_to_search = [col for col in selected_columns if col in df.columns]
    
    # Buscar en columnas seleccionadas
    for col_idx, column in enumerate(df.columns):
        if column not in columns_to_search:
            continue
            
        for row_idx, value in enumerate(df[column]):
            if pd.isna(value):
                continue
                
            # Convertir valor a string
            str_value = str(value)
            search_value = str_value.lower() if not case_sensitive else str_value
            
            # Buscar término
            if search_term in search_value:
                results.append({
                    'fila': row_idx + 2,  # +2 porque pandas empieza en 0 y Excel en 1, más header
                    'columna': column,
                    'columna_numero': col_idx + 1,  # +1 para que coincida con Excel
                    'texto_completo': str_value,
                    'contexto': get_context(df, row_idx, col_idx)
                })
    
    return results

def get_context(df, row_idx, col_idx):
    """Obtener contexto de la celda (celdas adyacentes)"""
    context = {}
    
    # Obtener algunas columnas del mismo row para contexto
    for i, col in enumerate(df.columns[:10]):  # Límite a 10 columnas para no sobrecargar
        if not pd.isna(df.iloc[row_idx, i]):
            context[col] = str(df.iloc[row_idx, i])
    
    return context

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_data, current_filename
    
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Cargar datos
            current_data = load_file(filepath)
            current_filename = filename
            
            # Eliminar archivo temporal
            os.remove(filepath)
            
            flash(f'Archivo {filename} cargado exitosamente. {len(current_data)} filas, {len(current_data.columns)} columnas.')
            return redirect(url_for('search_page'))
            
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}')
            return redirect(request.url)
    
    flash('Tipo de archivo no permitido. Use CSV, XLS o XLSX')
    return redirect(request.url)

@app.route('/search')
def search_page():
    if current_data is None:
        flash('Primero debe cargar un archivo')
        return redirect(url_for('index'))
    
    columns = list(current_data.columns)
    return render_template('search.html', 
                         filename=current_filename, 
                         columns=columns,
                         total_rows=len(current_data))

@app.route('/api/search', methods=['POST'])
def api_search():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No hay datos cargados'}), 400
    
    data = request.json
    search_term = data.get('search_term', '').strip()
    case_sensitive = data.get('case_sensitive', False)
    selected_columns = data.get('selected_columns', [])
    
    if not search_term:
        return jsonify({'error': 'Debe ingresar un término de búsqueda'}), 400
    
    try:
        results = search_in_dataframe(current_data, search_term, case_sensitive, selected_columns)
        
        return jsonify({
            'results': results,
            'total_results': len(results),
            'search_term': search_term,
            'searched_columns': selected_columns if selected_columns else list(current_data.columns)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error en la búsqueda: {str(e)}'}), 500

@app.route('/reset')
def reset():
    global current_data, current_filename
    current_data = None
    current_filename = None
    flash('Sesión reiniciada')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)