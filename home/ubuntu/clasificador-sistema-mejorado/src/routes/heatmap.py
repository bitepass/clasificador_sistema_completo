from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.heatmap_generator import HeatMapGenerator
from models.models import db

heatmap_bp = Blueprint('heatmap', __name__)

@heatmap_bp.route('/data', methods=['POST'])
def get_heatmap_data():
    """
    Obtener datos para el mapa de calor
    """
    try:
        data = request.get_json()
        
        partido = data.get('partido', 'San Martín')
        tipo_delito = data.get('tipo_delito', 'todos')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        generator = HeatMapGenerator(db.session)
        heatmap_data = generator.generate_heatmap_data(
            partido=partido,
            tipo_delito=tipo_delito,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        return jsonify({
            'success': True,
            'data': heatmap_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generando datos del mapa: {str(e)}'
        }), 500

@heatmap_bp.route('/image', methods=['POST'])
def generate_heatmap_image():
    """
    Generar imagen del mapa de calor
    """
    try:
        data = request.get_json()
        
        partido = data.get('partido', 'San Martín')
        tipo_delito = data.get('tipo_delito', 'todos')
        width = data.get('width', 800)
        height = data.get('height', 600)
        
        generator = HeatMapGenerator(db.session)
        image_data = generator.generate_heatmap_image(
            partido=partido,
            tipo_delito=tipo_delito,
            width=width,
            height=height
        )
        
        # Crear buffer con la imagen
        buffer = io.BytesIO(image_data)
        buffer.seek(0)
        
        filename = f"mapa_calor_{partido.lower().replace(' ', '_')}_{tipo_delito}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='image/png'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generando imagen del mapa: {str(e)}'
        }), 500

@heatmap_bp.route('/partidos', methods=['GET'])
def get_partidos():
    """
    Obtener lista de partidos disponibles para mapas de calor
    """
    try:
        generator = HeatMapGenerator(db.session)
        partidos = generator.get_available_partidos()
        
        return jsonify({
            'success': True,
            'partidos': partidos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error obteniendo partidos: {str(e)}'
        }), 500

@heatmap_bp.route('/partido/<string:partido>/info', methods=['GET'])
def get_partido_info(partido: str):
    """
    Obtener información detallada de un partido
    """
    try:
        generator = HeatMapGenerator(db.session)
        info = generator.get_partido_info(partido)
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error obteniendo información del partido: {str(e)}'
        }), 500

@heatmap_bp.route('/tipos-delito', methods=['GET'])
def get_tipos_delito():
    """
    Obtener tipos de delitos disponibles para filtrar
    """
    tipos = [
        {
            'value': 'todos',
            'label': 'Todos los delitos',
            'description': 'Incluye todos los tipos de delitos'
        },
        {
            'value': 'robos',
            'label': 'Robos',
            'description': 'Robos simples y agravados'
        },
        {
            'value': 'hurtos',
            'label': 'Hurtos',
            'description': 'Hurtos de automotores y otros'
        },
        {
            'value': 'lesiones',
            'label': 'Lesiones',
            'description': 'Lesiones dolosas y culposas'
        },
        {
            'value': 'homicidios',
            'label': 'Homicidios',
            'description': 'Homicidios simples y agravados'
        }
    ]
    
    return jsonify({
        'success': True,
        'tipos': tipos
    })

@heatmap_bp.route('/estadisticas/<string:partido>', methods=['GET'])
def get_estadisticas_partido(partido: str):
    """
    Obtener estadísticas generales de un partido
    """
    try:
        tipo_delito = request.args.get('tipo_delito', 'todos')
        
        generator = HeatMapGenerator(db.session)
        data = generator.generate_heatmap_data(partido, tipo_delito)
        
        estadisticas = {
            'partido': partido,
            'total_delitos': data['estadisticas']['total_delitos'],
            'promedio_por_zona': data['estadisticas']['promedio_por_zona'],
            'zona_mas_critica': data['estadisticas']['zona_mas_critica'],
            'zona_mas_segura': data['estadisticas']['zona_mas_segura'],
            'distribucion_intensidad': data['estadisticas']['distribucion_intensidad'],
            'total_zonas': len(data['zonas']),
            'fecha_actualizacion': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'estadisticas': estadisticas
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error obteniendo estadísticas: {str(e)}'
        }), 500

@heatmap_bp.route('/zona/<string:partido>/<string:zona>/detalles', methods=['GET'])
def get_zona_detalles(partido: str, zona: str):
    """
    Obtener detalles específicos de una zona
    """
    try:
        tipo_delito = request.args.get('tipo_delito', 'todos')
        
        generator = HeatMapGenerator(db.session)
        data = generator.generate_heatmap_data(partido, tipo_delito)
        
        # Buscar la zona específica
        zona_info = None
        for z in data['zonas']:
            if z['nombre'].lower() == zona.lower():
                zona_info = z
                break
        
        if not zona_info:
            return jsonify({
                'success': False,
                'error': f'Zona no encontrada: {zona}'
            }), 404
        
        # Agregar información adicional
        detalles = {
            'zona': zona_info,
            'ranking': None,  # Posición en ranking de criminalidad
            'tendencia': 'estable',  # Tendencia temporal
            'comparacion_promedio': None,  # Comparación con promedio del partido
            'recomendaciones': [
                'Incrementar patrullajes en horarios críticos',
                'Mejorar iluminación en vías públicas',
                'Coordinar con comerciantes locales'
            ]
        }
        
        # Calcular ranking
        zonas_ordenadas = sorted(data['zonas'], key=lambda x: x['delitos'], reverse=True)
        for i, z in enumerate(zonas_ordenadas):
            if z['nombre'] == zona_info['nombre']:
                detalles['ranking'] = i + 1
                break
        
        # Calcular comparación con promedio
        promedio = data['estadisticas']['promedio_por_zona']
        diferencia = zona_info['delitos'] - promedio
        porcentaje = (diferencia / promedio) * 100 if promedio > 0 else 0
        
        detalles['comparacion_promedio'] = {
            'diferencia': round(diferencia, 1),
            'porcentaje': round(porcentaje, 1),
            'estado': 'por encima' if diferencia > 0 else 'por debajo' if diferencia < 0 else 'igual'
        }
        
        return jsonify({
            'success': True,
            'detalles': detalles
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error obteniendo detalles de la zona: {str(e)}'
        }), 500

