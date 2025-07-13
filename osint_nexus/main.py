from __future__ import annotations

import json
from typing import Dict

import streamlit as st

from osint_nexus.utils.api_manager import APIManager
from osint_nexus.utils.pdf_report import generate_pdf
from osint_nexus.utils.graph_builder import build_graph_from_results
from osint_nexus.utils.retention import cleanup_files

# Importamos módulos dinámicamente
from importlib import import_module

from pathlib import Path

def discover_modules() -> Dict[str, str]:
    """Explora la carpeta de módulos en busca de archivos *_analysis.py."""
    modules_dir = Path(__file__).parent / "modules"
    registry: Dict[str, str] = {}
    for py_file in modules_dir.glob("*_analysis.py"):
        name = py_file.stem.replace("_analysis", "").capitalize()
        # Convierte "domain" en "Dominio", "email" en "Email", etc.
        friendly = name.replace("_", " ").title()
        registry[friendly] = py_file.stem
    return registry

MODULE_REGISTRY: Dict[str, str] = discover_modules()

# Configuración de la página
st.set_page_config(page_title="OSINT-Nexus", layout="wide")

st.title("🔍 OSINT-Nexus – Plataforma de Inteligencia Automatizada")

st.markdown(
    """
    *Herramienta didáctica para la automatización de investigaciones OSINT.  
    **Uso exclusivo con fines éticos y dentro del marco legal**. El usuario es responsable del cumplimiento de las leyes vigentes y de la protección de la privacidad de terceros.
    """
)

# Sidebar – Gestión de API Keys y políticas de datos
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

st.sidebar.header("🗑️ Retención de datos")
retention_hours = st.sidebar.number_input(
    "Horas antes de eliminar informes locales", min_value=1, max_value=168, value=24, step=1
)

# Limpiamos PDFs antiguos en background (al arrancar la app)
cleanup_files(Path.cwd(), "*.pdf", max_age_hours=int(retention_hours))

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

    # Muestra grafo de relaciones
    st.subheader("Grafo de relaciones (heurístico)")
    _, graph_fig = build_graph_from_results(
        st.session_state.last_context["target"], st.session_state.last_result
    )
    st.pyplot(graph_fig)

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