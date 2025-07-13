from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import streamlit as st

from osint_nexus.utils.api_manager import APIManager
from osint_nexus.utils.pdf_report import generate_pdf

# Importamos módulos dinámicamente
from importlib import import_module

MODULE_REGISTRY: Dict[str, str] = {
    "Dominio/IP": "domain_analysis",
    "Correo electrónico": "email_analysis",
    "Nombre de usuario": "username_analysis",
    "Perfil social": "social_analysis",
}

# Configuración de la página
st.set_page_config(page_title="OSINT-Nexus", layout="wide")

st.title("🔍 OSINT-Nexus – Plataforma de Inteligencia Automatizada")

st.markdown(
    """
    *Herramienta didáctica para la automatización de investigaciones OSINT.  
    **Uso exclusivo con fines éticos y dentro del marco legal**. El usuario es responsable del cumplimiento de las leyes vigentes y de la protección de la privacidad de terceros.
    """
)

# Sidebar – Gestión de API Keys
st.sidebar.header("🔑 Configuración de APIs")

api_key_inputs: Dict[str, str] = {}
for api_label in [
    "SHODAN_API_KEY",
    "CRIMINALIP_API_KEY",
    "HUNTER_API_KEY",
    "HIBP_API_KEY",
]:
    api_key_inputs[api_label] = st.sidebar.text_input(api_label, type="password")

api_manager = APIManager(initial_overrides=api_key_inputs)

with st.sidebar.expander("Claves cargadas", expanded=False):
    st.json(api_manager.available_keys())

# Selección de módulo y target
col1, col2 = st.columns([1, 3])
with col1:
    module_name = st.selectbox("Tipo de objetivo", list(MODULE_REGISTRY.keys()))
with col2:
    target_input = st.text_input("Valor del objetivo", placeholder="ejemplo.com | user@example.com | alias123 | https://twitter.com/…")

run_btn = st.button("🚀 Iniciar investigación")

# Resultado en session state
if "last_result" not in st.session_state:
    st.session_state.last_result = None
    st.session_state.last_context = {}

if run_btn and target_input:
    module_path = MODULE_REGISTRY[module_name]
    module = import_module(f"osint_nexus.modules.{module_path}")
    with st.spinner("Ejecutando módulo…"):
        result_data = module.run(target_input, api_manager)
    st.session_state.last_result = result_data
    st.session_state.last_context = {
        "module": module_name,
        "target": target_input,
    }

# Mostrar resultados
if st.session_state.last_result:
    st.subheader("Resultados de la investigación")

    # Dashboard con pestañas
    tabs = st.tabs(list(st.session_state.last_result.keys()))
    for tab, (section, content) in zip(tabs, st.session_state.last_result.items()):
        with tab:
            if isinstance(content, (dict, list)):
                st.json(content)
            else:
                st.write(content)

    # Botón de descarga en PDF
    if st.button("📄 Descargar informe PDF"):
        with st.spinner("Generando informe PDF…"):
            output_pdf = generate_pdf(
                st.session_state.last_context["module"],
                st.session_state.last_context["target"],
                st.session_state.last_result,
                Path("osint_report.pdf"),
            )
        with open(output_pdf, "rb") as f:
            st.download_button(
                label="Descargar informe",
                data=f,
                file_name=output_pdf.name,
                mime="application/pdf",
            )

# Footer
st.markdown(
    "---\nPowered by **OSINT-Nexus** · Código abierto bajo licencia MIT"
)