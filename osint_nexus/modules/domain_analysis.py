from __future__ import annotations

import requests
from typing import Dict, Any

from osint_nexus.utils.api_manager import APIManager

USER_AGENT = "OSINT-Nexus/0.1 (+https://github.com/example/osint-nexus)"
HEADERS = {"User-Agent": USER_AGENT}


class DomainAnalysisError(Exception):
    """Errores específicos del módulo de dominio."""


def _safe_get_json(url: str, params: dict | None = None, headers: dict | None = None) -> Any:
    try:
        resp = requests.get(url, params=params, headers=headers or HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as err:  # pylint: disable=broad-except
        return {"error": str(err)}


def run(target: str, api_manager: APIManager) -> Dict[str, Any]:
    """Ejecuta la investigación de dominio/IP.

    Parameters
    ----------
    target : str
        Dominio (ejemplo.com) o dirección IP.
    api_manager : APIManager
        Gestor con las claves de API.

    Returns
    -------
    Dict[str, Any]
        Datos consolidados.
    """
    data: Dict[str, Any] = {}

    # 1. Whois (fuente pública sin autenticación)
    whois_url = f"https://api.whois.vu/?q={target}"
    data["Whois"] = _safe_get_json(whois_url)

    # 2. Shodan
    shodan_key = api_manager.get("SHODAN_API_KEY")
    if shodan_key:
        shodan_url = f"https://api.shodan.io/shodan/host/{target}?key={shodan_key}"
        data["Shodan"] = _safe_get_json(shodan_url)
    else:
        data["Shodan"] = "SHODAN_API_KEY no configurada."

    # 3. urlscan.io submission (solo se acepta dominio/URL)
    try:
        submission = _safe_get_json(
            "https://urlscan.io/api/v1/scan/",
            params=None,
            headers={
                **HEADERS,
                "Content-Type": "application/json",
            },
        )
        data["urlscan.io"] = submission
    except Exception as _:
        data["urlscan.io"] = "Error al consultar urlscan.io"

    # 4. Criminal IP (requiere key)
    crim_key = api_manager.get("CRIMINALIP_API_KEY")
    if crim_key:
        headers = {**HEADERS, "x-api-key": crim_key}
        crim_url = f"https://api.criminalip.io/v1/ip/{target}"  # Ejemplo
        data["CriminalIP"] = _safe_get_json(crim_url, headers=headers)
    else:
        data["CriminalIP"] = "CRIMINALIP_API_KEY no configurada."

    return data