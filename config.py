"""
Configuración del Buscador de Excel/CSV
"""

import os

class Config:
    """Configuración principal de la aplicación"""
    
    # Configuración del servidor
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-cambiar-en-produccion'
    
    # Archivos
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Configuración de búsqueda
    MAX_RESULTS = 1000  # Máximo número de resultados a mostrar
    CONTEXT_COLUMNS = 10  # Máximo número de columnas en contexto
    
    # Configuración de encoding para CSV
    CSV_ENCODINGS = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
    
    # Configuración de interfaz
    COLUMNS_PER_PAGE = 8  # Columnas mostradas inicialmente
    
    # Configuración de pandas
    PANDAS_DISPLAY_MAX_COLUMNS = None
    PANDAS_DISPLAY_MAX_ROWS = None
    
    @staticmethod
    def init_app(app):
        """Inicializar configuración de la aplicación"""
        # Crear directorio de uploads si no existe
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Configurar pandas
        import pandas as pd
        pd.set_option('display.max_columns', Config.PANDAS_DISPLAY_MAX_COLUMNS)
        pd.set_option('display.max_rows', Config.PANDAS_DISPLAY_MAX_ROWS)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    HOST = '127.0.0.1'  # Solo localhost en producción
    
    # Configuración de seguridad mejorada
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'generar-clave-aleatoria-segura'
    
    # Límites más restrictivos
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB en producción
    MAX_RESULTS = 500  # Menos resultados para mejor rendimiento

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = 'test_uploads'
    
    # Configuración de pruebas
    MAX_RESULTS = 100
    CONTEXT_COLUMNS = 5

# Configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Configuración por defecto
DEFAULT_CONFIG = 'default'

def get_config(config_name=None):
    """Obtener configuración según el nombre"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or DEFAULT_CONFIG
    
    return config.get(config_name, config[DEFAULT_CONFIG])

# Configuración de mensajes
MESSAGES = {
    'file_uploaded': 'Archivo cargado exitosamente',
    'no_file_selected': 'No se seleccionó ningún archivo',
    'invalid_file_type': 'Tipo de archivo no permitido. Use CSV, XLS o XLSX',
    'file_processing_error': 'Error al procesar el archivo',
    'search_term_required': 'Debe ingresar un término de búsqueda',
    'no_data_loaded': 'No hay datos cargados',
    'no_results_found': 'No se encontraron resultados',
    'search_error': 'Error en la búsqueda',
    'session_reset': 'Sesión reiniciada',
    'load_file_first': 'Primero debe cargar un archivo'
}

# Configuración de estilos
STYLES = {
    'glassmorphism': {
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'container_bg': 'rgba(255, 255, 255, 0.15)',
        'blur': '20px',
        'border': '1px solid rgba(255, 255, 255, 0.2)',
        'text_color': 'white'
    },
    'dark': {
        'background': 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
        'container_bg': 'rgba(0, 0, 0, 0.3)',
        'blur': '15px',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'text_color': 'white'
    }
}

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}