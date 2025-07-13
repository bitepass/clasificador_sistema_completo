"""
Validadores para diferentes tipos de datos de entrada
"""

import re
import socket
from urllib.parse import urlparse
from utils.logger import setup_logger

logger = setup_logger("validators")

def validate_domain(domain: str) -> bool:
    """
    Valida si una cadena es un dominio válido
    
    Args:
        domain: Dominio a validar
        
    Returns:
        True si es válido, False en caso contrario
    """
    if not domain or len(domain) > 255:
        return False
    
    # Regex para validar dominio
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    
    return bool(domain_pattern.match(domain))

def validate_email(email: str) -> bool:
    """
    Valida si una cadena es un email válido
    
    Args:
        email: Email a validar
        
    Returns:
        True si es válido, False en caso contrario
    """
    if not email or len(email) > 254:
        return False
    
    # Regex para validar email
    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    return bool(email_pattern.match(email))

def validate_ip(ip: str) -> bool:
    """
    Valida si una cadena es una IP válida (IPv4 o IPv6)
    
    Args:
        ip: IP a validar
        
    Returns:
        True si es válida, False en caso contrario
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False

def validate_url(url: str) -> bool:
    """
    Valida si una cadena es una URL válida
    
    Args:
        url: URL a validar
        
    Returns:
        True si es válida, False en caso contrario
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_username(username: str) -> bool:
    """
    Valida si una cadena es un nombre de usuario válido
    
    Args:
        username: Username a validar
        
    Returns:
        True si es válido, False en caso contrario
    """
    if not username or len(username) < 1 or len(username) > 50:
        return False
    
    # Regex para validar username (alfanumérico, guiones, puntos, guiones bajos)
    username_pattern = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    return bool(username_pattern.match(username))

def validate_phone(phone: str) -> bool:
    """
    Valida si una cadena es un número de teléfono válido
    
    Args:
        phone: Teléfono a validar
        
    Returns:
        True si es válido, False en caso contrario
    """
    if not phone:
        return False
    
    # Limpiar el número de espacios y caracteres especiales
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    # Regex para validar teléfono (formato internacional)
    phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    
    return bool(phone_pattern.match(clean_phone))

def sanitize_input(input_str: str) -> str:
    """
    Sanitiza una cadena de entrada
    
    Args:
        input_str: Cadena a sanitizar
        
    Returns:
        Cadena sanitizada
    """
    if not input_str:
        return ""
    
    # Remover caracteres peligrosos
    sanitized = re.sub(r'[<>"\']', '', input_str.strip())
    
    return sanitized

def detect_input_type(input_str: str) -> str:
    """
    Detecta automáticamente el tipo de entrada
    
    Args:
        input_str: Cadena de entrada
        
    Returns:
        Tipo detectado ('domain', 'email', 'ip', 'url', 'username', 'phone', 'unknown')
    """
    if not input_str:
        return 'unknown'
    
    sanitized = sanitize_input(input_str)
    
    # Verificar en orden de prioridad
    if validate_email(sanitized):
        return 'email'
    elif validate_ip(sanitized):
        return 'ip'
    elif validate_url(sanitized):
        return 'url'
    elif validate_domain(sanitized):
        return 'domain'
    elif validate_phone(sanitized):
        return 'phone'
    elif validate_username(sanitized):
        return 'username'
    else:
        return 'unknown'

def get_validation_function(input_type: str):
    """
    Obtiene la función de validación correspondiente al tipo
    
    Args:
        input_type: Tipo de entrada
        
    Returns:
        Función de validación
    """
    validators = {
        'domain': validate_domain,
        'email': validate_email,
        'ip': validate_ip,
        'url': validate_url,
        'username': validate_username,
        'phone': validate_phone
    }
    
    return validators.get(input_type, lambda x: False)