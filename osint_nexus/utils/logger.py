"""
Sistema de logging para OSINT-Nexus
"""

import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Configura un logger para el sistema
    
    Args:
        name: Nombre del logger
        log_file: Archivo de log (opcional)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (si se especifica)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_investigation(target: str, module: str, status: str, results: dict = None):
    """
    Registra una investigación en el log
    
    Args:
        target: Objetivo de la investigación
        module: Módulo utilizado
        status: Estado de la investigación
        results: Resultados obtenidos (opcional)
    """
    logger = setup_logger("investigation")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = {
        "timestamp": timestamp,
        "target": target,
        "module": module,
        "status": status,
        "results_count": len(results) if results else 0
    }
    
    logger.info(f"Investigation: {log_entry}")
    
    if status == "error" and results:
        logger.error(f"Error details: {results}")
    elif status == "success" and results:
        logger.debug(f"Results: {results}")

# Logger principal del sistema
main_logger = setup_logger("osint_nexus", "logs/osint_nexus.log")