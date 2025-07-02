from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import io
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.report_generator import ReportGenerator
from models.models import db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """
    Generar informe situacional
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['partido', 'fechaInicio', 'fechaFin', 'tipoReporte', 'formato']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        partido = data['partido']
        fecha_inicio = data['fechaInicio']
        fecha_fin = data['fechaFin']
        tipo_reporte = data['tipoReporte']
        formato = data['formato']
        
        # Validar fechas
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
        
        # Generar informe
        generator = ReportGenerator(db.session)
        
        if tipo_reporte == 'situacional':
            report_data = generator.generate_situational_report(
                partido=partido,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                formato=formato
            )
        else:
            return jsonify({'error': f'Tipo de reporte no soportado: {tipo_reporte}'}), 400
        
        # Preparar respuesta
        filename = f"informe_{tipo_reporte}_{partido.lower().replace(' ', '_')}_{fecha_inicio}_{fecha_fin}.{formato}"
        
        # Determinar content type
        content_type = {
            'pdf': 'application/pdf',
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }.get(formato, 'application/octet-stream')
        
        # Crear buffer con los datos
        buffer = io.BytesIO(report_data)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype=content_type
        )
        
    except Exception as e:
        return jsonify({'error': f'Error generando informe: {str(e)}'}), 500

@reports_bp.route('/report-templates', methods=['GET'])
def get_report_templates():
    """
    Obtener plantillas de informes disponibles
    """
    templates = [
        {
            'id': 'situacional',
            'nombre': 'Informe Situacional',
            'descripcion': 'Análisis completo de delitos por período',
            'formatos': ['pdf', 'word'],
            'campos_requeridos': ['partido', 'fechaInicio', 'fechaFin']
        },
        {
            'id': 'estadistico',
            'nombre': 'Reporte Estadístico',
            'descripcion': 'Datos numéricos y tendencias',
            'formatos': ['pdf', 'excel'],
            'campos_requeridos': ['partido', 'fechaInicio', 'fechaFin']
        },
        {
            'id': 'comparativo',
            'nombre': 'Análisis Comparativo',
            'descripcion': 'Comparación entre períodos',
            'formatos': ['pdf', 'word', 'excel'],
            'campos_requeridos': ['partido', 'fechaInicio', 'fechaFin', 'fechaComparacion']
        },
        {
            'id': 'ejecutivo',
            'nombre': 'Resumen Ejecutivo',
            'descripcion': 'Síntesis para autoridades',
            'formatos': ['pdf'],
            'campos_requeridos': ['partido', 'fechaInicio', 'fechaFin']
        }
    ]
    
    return jsonify({'templates': templates})

@reports_bp.route('/partidos', methods=['GET'])
def get_partidos():
    """
    Obtener lista de partidos disponibles
    """
    partidos = [
        'San Martín',
        'José C. Paz',
        'Malvinas Argentinas',
        'San Miguel',
        'Tres de Febrero',
        'Hurlingham',
        'Ituzaingó',
        'Morón',
        'General San Martín'
    ]
    
    return jsonify({'partidos': partidos})

@reports_bp.route('/report-history', methods=['GET'])
def get_report_history():
    """
    Obtener historial de informes generados
    """
    # En implementación real, esto consultaría la base de datos
    history = [
        {
            'id': 1,
            'tipo': 'situacional',
            'partido': 'San Martín',
            'periodo': 'Mayo 2025',
            'fecha_generacion': '2025-06-01T10:30:00Z',
            'formato': 'pdf',
            'tamaño': '2.3 MB',
            'estado': 'completado'
        },
        {
            'id': 2,
            'tipo': 'situacional',
            'partido': 'José C. Paz',
            'periodo': 'Mayo 2025',
            'fecha_generacion': '2025-06-01T11:15:00Z',
            'formato': 'word',
            'tamaño': '1.8 MB',
            'estado': 'completado'
        }
    ]
    
    return jsonify({'history': history})

@reports_bp.route('/preview-data', methods=['POST'])
def preview_report_data():
    """
    Obtener vista previa de los datos para el informe
    """
    try:
        data = request.get_json()
        
        partido = data.get('partido')
        fecha_inicio = data.get('fechaInicio')
        fecha_fin = data.get('fechaFin')
        
        if not all([partido, fecha_inicio, fecha_fin]):
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400
        
        # Generar datos de vista previa
        generator = ReportGenerator(db.session)
        preview_data = generator._get_report_data(partido, fecha_inicio, fecha_fin)
        
        # Simplificar datos para vista previa
        preview = {
            'partido': preview_data['partido'],
            'periodo': preview_data['periodo'],
            'total_delitos': preview_data['total_delitos'],
            'delito_principal': preview_data['delito_principal'],
            'distribucion_delitos': preview_data['distribucion_delitos'][:5],  # Solo top 5
            'estadisticas_resumen': {
                'homicidios': preview_data['estadisticas_generales']['homicidios'],
                'robos': preview_data['estadisticas_generales']['robos'],
                'hurtos': preview_data['estadisticas_generales']['hurtos']
            }
        }
        
        return jsonify({'preview': preview})
        
    except Exception as e:
        return jsonify({'error': f'Error generando vista previa: {str(e)}'}), 500

