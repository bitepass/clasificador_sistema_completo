#!/usr/bin/env python3
"""
🧪 Mini servidor para probar el frontend DDIC-SM
Sin dependencias externas, solo stdlib de Python
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from pathlib import Path

class DDICHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para simular las APIs"""
    
    def __init__(self, *args, **kwargs):
        # Cambiar al directorio static para servir archivos
        os.chdir('src/static')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Maneja requests GET"""
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/reports':
            self.path = '/reports.html'
        elif self.path.startswith('/api/'):
            self.handle_api_get()
            return
        
        super().do_GET()
    
    def do_POST(self):
        """Maneja requests POST (APIs simuladas)"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def handle_api_get(self):
        """Simula respuestas GET de las APIs"""
        responses = {
            '/api/clasificador/status/1': {
                'planilla_id': 1,
                'estado': 'COMPLETADO',
                'total_registros': 100,
                'registros_procesados': 100,
                'progreso': 100,
                'tiempo_estimado': 0,
                'nombre_archivo': 'test.xlsx'
            },
            '/api/reports/report-templates': {
                'templates': [
                    {
                        'id': 'situacional',
                        'nombre': 'Informe Situacional',
                        'descripcion': 'Análisis completo de delitos',
                        'formatos': ['pdf', 'word']
                    }
                ]
            },
            '/api/reports/partidos': {
                'partidos': ['San Martín', 'José C. Paz', 'Malvinas Argentinas']
            }
        }
        
        response_data = responses.get(self.path, {'error': 'API simulada'})
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(response_data).encode())
    
    def handle_api_post(self):
        """Simula respuestas POST de las APIs"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        responses = {
            '/api/clasificador/upload': {
                'success': True,
                'planilla_id': 1,
                'filename': 'test.xlsx',
                'total_filas': 100,
                'message': 'Archivo subido correctamente (simulado)'
            },
            '/api/clasificador/process/1': {
                'success': True,
                'message': 'Procesamiento iniciado (simulado)',
                'planilla_id': 1
            },
            '/api/clasificador/cancel/1': {
                'success': True,
                'message': 'Procesamiento cancelado (simulado)'
            },
            '/api/reports/preview-data': {
                'preview': {
                    'partido': 'San Martín',
                    'periodo': 'Mayo 2024',
                    'total_delitos': 150,
                    'delito_principal': 'Robo',
                    'distribucion_delitos': [
                        {'tipo': 'Robo', 'cantidad': 50, 'porcentaje': 33},
                        {'tipo': 'Hurto', 'cantidad': 30, 'porcentaje': 20}
                    ],
                    'estadisticas_resumen': {
                        'homicidios': 2,
                        'robos': 50,
                        'hurtos': 30
                    }
                }
            },
            '/api/reports/generate-report': {
                'success': True,
                'message': 'Informe generado (simulado)'
            }
        }
        
        # Buscar respuesta que coincida con el path
        response_data = None
        for path_pattern, data in responses.items():
            if self.path.startswith(path_pattern):
                response_data = data
                break
        
        if not response_data:
            response_data = {'success': False, 'error': 'API simulada no encontrada'}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(response_data).encode())
    
    def do_OPTIONS(self):
        """Maneja preflight requests de CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_test_server():
    """Inicia el servidor de prueba"""
    PORT = 5000
    
    print(f"""
🎯 DDIC-SM - SERVIDOR DE PRUEBA
{'='*50}
🚀 Iniciando servidor en puerto {PORT}...
📱 Frontend: http://localhost:{PORT}
📊 Informes: http://localhost:{PORT}/reports.html
🔌 APIs: Simuladas (respuestas fake)
{'='*50}
💡 Presiona Ctrl+C para detener
    """)
    
    try:
        with socketserver.TCPServer(("", PORT), DDICHandler) as httpd:
            print(f"✅ Servidor iniciado en http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('src/static/index.html'):
        print("❌ Error: Ejecutar desde el directorio build/app")
        print("💡 cd clasificador-delitos-produccion/build/app")
        exit(1)
    
    start_test_server()