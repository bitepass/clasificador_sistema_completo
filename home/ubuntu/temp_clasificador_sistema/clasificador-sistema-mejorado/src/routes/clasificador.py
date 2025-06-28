from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import io
import os
import pandas as pd
from werkzeug.utils import secure_filename
from src.models.models import db, Planilla, HechoDelictivo
import threading
import time

clasificador_bp = Blueprint('clasificador', __name__)

# Variables globales para el estado del procesamiento
processing_status = {}
processing_threads = {}

@clasificador_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Subir archivo Excel para procesar
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Formato de archivo no válido'}), 400
        
        # Leer el archivo Excel
        try:
            df = pd.read_excel(file)
            total_filas = len(df)
        except Exception as e:
            return jsonify({'error': f'Error leyendo archivo Excel: {str(e)}'}), 400
        
        # Crear registro en la base de datos
        planilla = Planilla(
            nombre_archivo=secure_filename(file.filename),
            fecha_subida=datetime.now(),
            total_registros=total_filas,
            estado='SUBIDO'
        )
        
        db.session.add(planilla)
        db.session.commit()
        
        # Inicializar estado de procesamiento
        processing_status[planilla.id] = {
            'estado': 'SUBIDO',
            'progreso': 0,
            'registros_procesados': 0,
            'tiempo_estimado': total_filas * 1.5,  # 1.5 segundos por fila
            'mensaje': 'Archivo subido correctamente'
        }
        
        return jsonify({
            'success': True,
            'planilla_id': planilla.id,
            'total_filas': total_filas,
            'filename': file.filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Error subiendo archivo: {str(e)}'}), 500

@clasificador_bp.route('/process/<int:planilla_id>', methods=['POST'])
def process_planilla(planilla_id):
    """
    Iniciar procesamiento de una planilla
    """
    try:
        planilla = Planilla.query.get(planilla_id)
        if not planilla:
            return jsonify({'error': 'Planilla no encontrada'}), 404
        
        if planilla_id in processing_threads and processing_threads[planilla_id].is_alive():
            return jsonify({'error': 'La planilla ya se está procesando'}), 400
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=process_planilla_background, args=(planilla_id,))
        thread.start()
        processing_threads[planilla_id] = thread
        
        # Actualizar estado
        processing_status[planilla_id] = {
            'estado': 'PROCESANDO',
            'progreso': 0,
            'registros_procesados': 0,
            'tiempo_estimado': planilla.total_registros * 1.5,
            'mensaje': 'Iniciando procesamiento...'
        }
        
        planilla.estado = 'PROCESANDO'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Procesamiento iniciado',
            'planilla_id': planilla_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error iniciando procesamiento: {str(e)}'}), 500

def process_planilla_background(planilla_id):
    """
    Procesar planilla en segundo plano
    """
    try:
        planilla = Planilla.query.get(planilla_id)
        total_registros = planilla.total_registros
        
        # Simular procesamiento
        for i in range(total_registros):
            if processing_status.get(planilla_id, {}).get('estado') == 'CANCELADO':
                break
            
            # Simular tiempo de procesamiento
            time.sleep(0.1)  # Reducido para demostración
            
            # Actualizar progreso
            progreso = ((i + 1) / total_registros) * 100
            processing_status[planilla_id] = {
                'estado': 'PROCESANDO',
                'progreso': progreso,
                'registros_procesados': i + 1,
                'tiempo_estimado': (total_registros - i - 1) * 0.1,
                'mensaje': f'Procesando registro {i + 1} de {total_registros}'
            }
        
        # Completar procesamiento
        if processing_status.get(planilla_id, {}).get('estado') != 'CANCELADO':
            processing_status[planilla_id] = {
                'estado': 'COMPLETADO',
                'progreso': 100,
                'registros_procesados': total_registros,
                'tiempo_estimado': 0,
                'mensaje': 'Procesamiento completado'
            }
            
            planilla.estado = 'COMPLETADO'
            planilla.registros_procesados = total_registros
            db.session.commit()
        
    except Exception as e:
        processing_status[planilla_id] = {
            'estado': 'ERROR',
            'progreso': 0,
            'registros_procesados': 0,
            'tiempo_estimado': 0,
            'mensaje': f'Error: {str(e)}'
        }
        
        planilla.estado = 'ERROR'
        db.session.commit()

@clasificador_bp.route('/status/<int:planilla_id>', methods=['GET'])
def get_processing_status(planilla_id):
    """
    Obtener estado del procesamiento
    """
    try:
        status = processing_status.get(planilla_id, {
            'estado': 'NO_ENCONTRADO',
            'progreso': 0,
            'registros_procesados': 0,
            'tiempo_estimado': 0,
            'mensaje': 'Estado no encontrado'
        })
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo estado: {str(e)}'}), 500

@clasificador_bp.route('/cancel/<int:planilla_id>', methods=['POST'])
def cancel_processing(planilla_id):
    """
    Cancelar procesamiento
    """
    try:
        if planilla_id in processing_status:
            processing_status[planilla_id]['estado'] = 'CANCELADO'
            processing_status[planilla_id]['mensaje'] = 'Proceso cancelado por el usuario'
        
        planilla = Planilla.query.get(planilla_id)
        if planilla:
            planilla.estado = 'CANCELADO'
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Procesamiento cancelado'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error cancelando procesamiento: {str(e)}'}), 500

@clasificador_bp.route('/generate-excel/<int:planilla_id>', methods=['GET'])
def generate_excel(planilla_id):
    """
    Generar archivo Excel con resultados clasificados
    """
    try:
        planilla = Planilla.query.get(planilla_id)
        if not planilla:
            return jsonify({'error': 'Planilla no encontrada'}), 404
        
        if planilla.estado != 'COMPLETADO':
            return jsonify({'error': 'La planilla no ha sido procesada completamente'}), 400
        
        # Simular generación de Excel con datos clasificados
        # En implementación real, esto consultaría la base de datos
        data = {
            'id_hecho': [f'H{i:04d}' for i in range(1, planilla.total_registros + 1)],
            'nro_registro': [f'R{i:06d}' for i in range(1, planilla.total_registros + 1)],
            'fecha_hecho': ['2025-05-15'] * planilla.total_registros,
            'calificacion': ['ROBO_SIMPLE'] * planilla.total_registros,
            'jurisdiccion': ['URBANA'] * planilla.total_registros,
            'modalidad': ['ASALTO_VIA_PUBLICA'] * planilla.total_registros,
            'victimas': ['MASCULINO'] * planilla.total_registros,
            'armas': ['NINGUNA'] * planilla.total_registros,
            'lugar': ['VIA_PUBLICA'] * planilla.total_registros
        }
        
        df = pd.DataFrame(data)
        
        # Crear buffer para el archivo Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Clasificados')
        
        buffer.seek(0)
        
        filename = f"clasificado_{planilla.nombre_archivo}"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error generando Excel: {str(e)}'}), 500

@clasificador_bp.route('/planillas', methods=['GET'])
def get_planillas():
    """
    Obtener lista de planillas
    """
    try:
        planillas = Planilla.query.order_by(Planilla.fecha_subida.desc()).all()
        
        result = []
        for planilla in planillas:
            result.append({
                'id': planilla.id,
                'nombre_archivo': planilla.nombre_archivo,
                'fecha_subida': planilla.fecha_subida.isoformat(),
                'total_registros': planilla.total_registros,
                'registros_procesados': planilla.registros_procesados or 0,
                'estado': planilla.estado,
                'progreso': processing_status.get(planilla.id, {}).get('progreso', 0)
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo planillas: {str(e)}'}), 500

