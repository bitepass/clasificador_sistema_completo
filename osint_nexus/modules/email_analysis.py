import requests
from typing import Dict, Any

from osint_nexus.utils.api_manager import APIManager

HEADERS = {"User-Agent": "OSINT-Nexus/0.1"}


def _safe_get_json(url: str, params: dict | None = None, headers: dict | None = None) -> Any:
    try:
        resp = requests.get(url, params=params, headers=headers or HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as err:  # pylint: disable=broad-except
        return {"error": str(err)}


def run(target: str, api_manager: APIManager) -> Dict[str, Any]:
    """Analiza un correo electrónico."""
    data: Dict[str, Any] = {}

    # Hunter.io
    hunter_key = api_manager.get("HUNTER_API_KEY")
    if hunter_key:
        hunter_url = "https://api.hunter.io/v2/email-verifier"
        data["Hunter.io"] = _safe_get_json(hunter_url, params={"email": target, "api_key": hunter_key})
    else:
        data["Hunter.io"] = "HUNTER_API_KEY no configurada."

    # Have I Been Pwned
    hibp_key = api_manager.get("HIBP_API_KEY")
    hibp_headers = {**HEADERS}
    if hibp_key:
        hibp_headers["hibp-api-key"] = hibp_key
    hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}"
    resp = requests.get(hibp_url, headers=hibp_headers, timeout=10)
    if resp.status_code == 200:
        data["HIBP"] = resp.json()
    elif resp.status_code == 404:
        data["HIBP"] = "No se encontraron brechas para el correo."
    else:
        data["HIBP"] = f"HIBP error: {resp.status_code}"

    # Epieos (busqueda inversa). No requiere clave pero limita solicitudes.
    epieos_url = f"https://epieos.com/api/email/{target}"
    data["Epieos"] = _safe_get_json(epieos_url)

    return data