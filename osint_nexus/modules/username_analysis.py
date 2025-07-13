import requests
from typing import Dict, Any

from osint_nexus.utils.api_manager import APIManager

HEADERS = {"User-Agent": "OSINT-Nexus/0.1"}

NAMECHK_URL = "https://namechk.com/services/api/username/"


def _safe_get_json(url: str, params: dict | None = None) -> Any:
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as err:  # pylint: disable=broad-except
        return {"error": str(err)}


def run(target: str, api_manager: APIManager) -> Dict[str, Any]:
    """Busca un nombre de usuario en diferentes plataformas.

    Esta implementación usa solo Namechk (API no oficial) como ejemplo.
    Para resultados más completos se recomienda integrar Sherlock o Blackbird
    como procesos externos.
    """
    data: Dict[str, Any] = {}

    namechk_resp = _safe_get_json(NAMECHK_URL + target)
    data["Namechk"] = namechk_resp

    # Lugares para integrar Sherlock/Blackbird (requiere ejecutarlos como subproceso)
    data["Sherlock"] = "Integración no implementada en esta versión."

    return data