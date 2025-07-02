import json
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from io import BytesIO
import base64

class HeatMapGenerator:
    def __init__(self, db_session):
        self.db = db_session
        self.partidos_coords = {
            'San Martín': {
                'center': (-34.5722, -58.5358),
                'bounds': {
                    'north': -34.5500,
                    'south': -34.5900,
                    'east': -58.5100,
                    'west': -58.5600
                },
                'zonas': [
                    {'nombre': 'Centro', 'lat': -34.5722, 'lng': -58.5358},
                    {'nombre': 'Villa Ballester', 'lat': -34.5489, 'lng': -58.5503},
                    {'nombre': 'Chilavert', 'lat': -34.5856, 'lng': -58.5167},
                    {'nombre': 'Villa Maipú', 'lat': -34.5611, 'lng': -58.5444},
                    {'nombre': 'José León Suárez', 'lat': -34.5333, 'lng': -58.5667}
                ]
            },
            'José C. Paz': {
                'center': (-34.5200, -58.7600),
                'bounds': {
                    'north': -34.5000,
                    'south': -34.5400,
                    'east': -58.7300,
                    'west': -58.7900
                },
                'zonas': [
                    {'nombre': 'Centro', 'lat': -34.5200, 'lng': -58.7600},
                    {'nombre': 'Barrio Norte', 'lat': -34.5100, 'lng': -58.7500},
                    {'nombre': 'Barrio Sur', 'lat': -34.5300, 'lng': -58.7700},
                    {'nombre': 'Villa Altube', 'lat': -34.5150, 'lng': -58.7650},
                    {'nombre': 'Frino', 'lat': -34.5250, 'lng': -58.7550}
                ]
            },
            'Malvinas Argentinas': {
                'center': (-34.4600, -58.7000),
                'bounds': {
                    'north': -34.4300,
                    'south': -34.4900,
                    'east': -58.6700,
                    'west': -58.7300
                },
                'zonas': [
                    {'nombre': 'Los Polvorines', 'lat': -34.4600, 'lng': -58.7000},
                    {'nombre': 'Grand Bourg', 'lat': -34.4700, 'lng': -58.7200},
                    {'nombre': 'Villa de Mayo', 'lat': -34.4500, 'lng': -58.6900},
                    {'nombre': 'Tortuguitas', 'lat': -34.4400, 'lng': -58.7100},
                    {'nombre': 'Pablo Nogués', 'lat': -34.4800, 'lng': -58.7000}
                ]
            },
            'San Miguel': {
                'center': (-34.5400, -58.7100),
                'bounds': {
                    'north': -34.5200,
                    'south': -34.5600,
                    'east': -58.6800,
                    'west': -58.7400
                },
                'zonas': [
                    {'nombre': 'Centro', 'lat': -34.5400, 'lng': -58.7100},
                    {'nombre': 'Bella Vista', 'lat': -34.5500, 'lng': -58.6900},
                    {'nombre': 'Muñiz', 'lat': -34.5300, 'lng': -58.7200},
                    {'nombre': 'Santa María', 'lat': -34.5450, 'lng': -58.7050},
                    {'nombre': 'Tierras Altas', 'lat': -34.5350, 'lng': -58.7150}
                ]
            }
        }
    
    def generate_heatmap_data(self, 
                            partido: str, 
                            tipo_delito: str = 'todos',
                            fecha_inicio: Optional[str] = None,
                            fecha_fin: Optional[str] = None) -> Dict[str, Any]:
        """
        Generar datos para el mapa de calor
        """
        if partido not in self.partidos_coords:
            raise ValueError(f"Partido no soportado: {partido}")
        
        partido_info = self.partidos_coords[partido]
        zonas_data = []
        
        for zona in partido_info['zonas']:
            # Simular datos de delitos por zona
            delitos_data = self._generate_zone_crime_data(zona['nombre'], tipo_delito)
            
            zona_info = {
                'id': len(zonas_data) + 1,
                'nombre': zona['nombre'],
                'coordenadas': {
                    'lat': zona['lat'],
                    'lng': zona['lng']
                },
                'delitos': delitos_data['total'],
                'intensidad': self._calculate_intensity(delitos_data['total']),
                'tipos': delitos_data['tipos'],
                'detalles': delitos_data['detalles']
            }
            zonas_data.append(zona_info)
        
        return {
            'partido': partido,
            'centro': partido_info['center'],
            'bounds': partido_info['bounds'],
            'zonas': zonas_data,
            'estadisticas': self._calculate_general_stats(zonas_data),
            'metadata': {
                'fecha_generacion': datetime.now().isoformat(),
                'tipo_delito': tipo_delito,
                'total_zonas': len(zonas_data)
            }
        }
    
    def _generate_zone_crime_data(self, zona_nombre: str, tipo_delito: str) -> Dict[str, Any]:
        """
        Generar datos de delitos para una zona específica
        """
        # Factores de criminalidad por zona (simulado)
        zone_factors = {
            'Centro': 1.5,
            'Villa Ballester': 1.2,
            'Chilavert': 0.8,
            'Villa Maipú': 0.6,
            'José León Suárez': 1.8,
            'Barrio Norte': 1.1,
            'Barrio Sur': 1.4,
            'Villa Altube': 0.9,
            'Frino': 1.0,
            'Los Polvorines': 1.3,
            'Grand Bourg': 1.1,
            'Villa de Mayo': 0.7,
            'Tortuguitas': 0.5,
            'Pablo Nogués': 1.0,
            'Bella Vista': 0.8,
            'Muñiz': 1.2,
            'Santa María': 0.9,
            'Tierras Altas': 0.6
        }
        
        factor = zone_factors.get(zona_nombre, 1.0)
        base_crimes = int(random.uniform(15, 50) * factor)
        
        # Distribución por tipo de delito
        if tipo_delito == 'todos':
            tipos = {
                'robos': int(base_crimes * 0.6),
                'hurtos': int(base_crimes * 0.25),
                'lesiones': int(base_crimes * 0.10),
                'otros': int(base_crimes * 0.05)
            }
        elif tipo_delito == 'robos':
            tipos = {
                'robos': base_crimes,
                'hurtos': 0,
                'lesiones': 0,
                'otros': 0
            }
        elif tipo_delito == 'hurtos':
            tipos = {
                'robos': 0,
                'hurtos': base_crimes,
                'lesiones': 0,
                'otros': 0
            }
        else:
            tipos = {
                'robos': int(base_crimes * 0.6),
                'hurtos': int(base_crimes * 0.25),
                'lesiones': int(base_crimes * 0.10),
                'otros': int(base_crimes * 0.05)
            }
        
        total = sum(tipos.values())
        
        return {
            'total': total,
            'tipos': tipos,
            'detalles': {
                'horarios_criticos': ['18:00-22:00', '02:00-06:00'],
                'dias_semana': ['viernes', 'sábado', 'domingo'],
                'modalidades_principales': [
                    'Asalto en vía pública',
                    'Hurto de automotor',
                    'Robo en comercio'
                ]
            }
        }
    
    def _calculate_intensity(self, total_delitos: int) -> str:
        """
        Calcular la intensidad basada en el total de delitos
        """
        if total_delitos >= 30:
            return 'alta'
        elif total_delitos >= 15:
            return 'media'
        else:
            return 'baja'
    
    def _calculate_general_stats(self, zonas_data: List[Dict]) -> Dict[str, Any]:
        """
        Calcular estadísticas generales del mapa
        """
        total_delitos = sum(zona['delitos'] for zona in zonas_data)
        total_robos = sum(zona['tipos']['robos'] for zona in zonas_data)
        total_hurtos = sum(zona['tipos']['hurtos'] for zona in zonas_data)
        
        zona_mas_critica = max(zonas_data, key=lambda x: x['delitos'])
        zona_mas_segura = min(zonas_data, key=lambda x: x['delitos'])
        
        return {
            'total_delitos': total_delitos,
            'promedio_por_zona': round(total_delitos / len(zonas_data), 1),
            'zona_mas_critica': {
                'nombre': zona_mas_critica['nombre'],
                'delitos': zona_mas_critica['delitos']
            },
            'zona_mas_segura': {
                'nombre': zona_mas_segura['nombre'],
                'delitos': zona_mas_segura['delitos']
            },
            'distribucion_intensidad': {
                'alta': len([z for z in zonas_data if z['intensidad'] == 'alta']),
                'media': len([z for z in zonas_data if z['intensidad'] == 'media']),
                'baja': len([z for z in zonas_data if z['intensidad'] == 'baja'])
            },
            'tipos_principales': {
                'robos': total_robos,
                'hurtos': total_hurtos,
                'porcentaje_robos': round((total_robos / total_delitos) * 100, 1) if total_delitos > 0 else 0
            }
        }
    
    def generate_heatmap_image(self, 
                             partido: str, 
                             tipo_delito: str = 'todos',
                             width: int = 800,
                             height: int = 600) -> bytes:
        """
        Generar imagen del mapa de calor
        """
        data = self.generate_heatmap_data(partido, tipo_delito)
        
        # Configurar matplotlib para no usar GUI
        plt.switch_backend('Agg')
        
        fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
        
        # Configurar límites del mapa
        bounds = data['bounds']
        ax.set_xlim(bounds['west'], bounds['east'])
        ax.set_ylim(bounds['south'], bounds['north'])
        
        # Crear colormap personalizado
        colors = ['#10b981', '#f59e0b', '#ef4444']  # verde, amarillo, rojo
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('crime_intensity', colors, N=n_bins)
        
        # Dibujar zonas
        for zona in data['zonas']:
            lat = zona['coordenadas']['lat']
            lng = zona['coordenadas']['lng']
            delitos = zona['delitos']
            
            # Normalizar intensidad (0-1)
            max_delitos = max(z['delitos'] for z in data['zonas'])
            intensity = delitos / max_delitos if max_delitos > 0 else 0
            
            # Tamaño del círculo proporcional a los delitos
            size = max(delitos * 20, 100)
            
            # Color basado en intensidad
            color = cmap(intensity)
            
            # Dibujar círculo
            circle = plt.Circle((lng, lat), size/100000, color=color, alpha=0.7)
            ax.add_patch(circle)
            
            # Agregar etiqueta
            ax.annotate(
                f"{zona['nombre']}\n{delitos}",
                (lng, lat),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8,
                ha='left',
                va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
            )
        
        # Configurar título y etiquetas
        ax.set_title(f'Mapa de Calor - {partido}\nTipo: {tipo_delito.title()}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitud', fontsize=10)
        ax.set_ylabel('Latitud', fontsize=10)
        
        # Agregar leyenda
        legend_elements = [
            plt.Circle((0, 0), 1, color='#ef4444', alpha=0.7, label='Alta (30+)'),
            plt.Circle((0, 0), 1, color='#f59e0b', alpha=0.7, label='Media (15-29)'),
            plt.Circle((0, 0), 1, color='#10b981', alpha=0.7, label='Baja (1-14)')
        ]
        ax.legend(handles=legend_elements, loc='upper right', title='Intensidad')
        
        # Configurar grid
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Guardar en buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def get_available_partidos(self) -> List[str]:
        """
        Obtener lista de partidos disponibles
        """
        return list(self.partidos_coords.keys())
    
    def get_partido_info(self, partido: str) -> Dict[str, Any]:
        """
        Obtener información detallada de un partido
        """
        if partido not in self.partidos_coords:
            raise ValueError(f"Partido no encontrado: {partido}")
        
        info = self.partidos_coords[partido].copy()
        info['nombre'] = partido
        info['total_zonas'] = len(info['zonas'])
        
        return info

