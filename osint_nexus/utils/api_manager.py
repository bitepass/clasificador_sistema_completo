import os
from typing import Optional
from dotenv import load_dotenv

# Cargamos variables de entorno desde .env si existe
load_dotenv()

class APIManager:
    """Gestor centralizado de claves de API.

    1. Intenta obtener las claves desde variables de entorno.
    2. Permite actualizar claves en caliente (por ejemplo, desde Streamlit sidebar).
    """

    def __init__(self, initial_overrides: Optional[dict] = None):
        self._keys: dict[str, str] = {}
        # Cargamos todas las variables de entorno que terminan en _API_KEY
        for k, v in os.environ.items():
            if k.endswith("_API_KEY"):
                self._keys[k] = v
        # Aplicamos overrides iniciales, típicamente proporcionados por Streamlit
        if initial_overrides:
            self._keys.update({k: v for k, v in initial_overrides.items() if v})

    def get(self, key_name: str) -> Optional[str]:
        """Devuelve la clave o None si no está definida."""
        return self._keys.get(key_name)

    def set(self, key_name: str, value: str) -> None:
        """Actualiza/crea una clave de API para la sesión actual."""
        if not key_name.endswith("_API_KEY"):
            key_name += "_API_KEY"
        self._keys[key_name] = value

    def available_keys(self) -> dict[str, str]:
        """Devuelve un diccionario con las claves disponibles (valores censurados)."""
        hidden = {}
        for k, v in self._keys.items():
            if not v:
                continue
            hidden[k] = v[:3] + "***" + v[-2:]  # Ocultamos parte de la clave
        return hidden