"""
OSINT-NEXUS - Plataforma de Inteligencia Automatizada
Aplicación principal con interfaz Streamlit
"""

import streamlit as st
import asyncio
import json
import base64
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import os

# Importar módulos propios
from modules.domain_analysis import DomainAnalyzer
from modules.email_investigation import EmailInvestigator
from modules.username_search import UsernameSearcher
from utils.data_processor import DataProcessor
from utils.report_generator import ReportGenerator
from config.api_keys import APIConfig

# Configuración de la página
st.set_page_config(
    page_title="OSINT-NEXUS",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para una interfaz moderna
st.markdown("""
<style>
    /* Tema oscuro profesional */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Título principal */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
    }
    
    /* Subtítulo */
    .sub-header {
        font-size: 1.2rem;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Tarjetas de resultados */
    .result-card {
        background-color: #1e2329;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #2d3139;
    }
    
    /* Métricas destacadas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        color: white;
    }
    
    /* Botón de búsqueda */
    .stButton > button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border-radius: 25px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #1e2329;
        border: 1px solid #2d3139;
        border-radius: 8px;
        color: white;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background-color: #1e2329;
        border: 1px solid #2d3139;
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e2329;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a0a0a0;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3a7bd5;
        color: white;
    }
    
    /* Alertas */
    .success-alert {
        background-color: #27ae60;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-alert {
        background-color: #f39c12;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-alert {
        background-color: #e74c3c;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if 'investigations' not in st.session_state:
    st.session_state.investigations = []
if 'current_investigation' not in st.session_state:
    st.session_state.current_investigation = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Función para ejecutar investigaciones asíncronas
def run_async(coro):
    """Ejecutar corutina asíncrona"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# Header principal
st.markdown('<h1 class="main-header">OSINT-NEXUS</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma de Inteligencia de Fuentes Abiertas</p>', unsafe_allow_html=True)

# Sidebar para configuración
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    # Verificar APIs configuradas
    st.markdown("#### 🔑 APIs Configuradas")
    apis = ['shodan', 'hunter', 'hibp', 'criminal_ip', 'urlscan']
    api_status = {}
    
    for api in apis:
        if APIConfig.is_api_configured(api):
            st.success(f"✅ {api.upper()}")
            api_status[api] = True
        else:
            st.warning(f"❌ {api.upper()}")
            api_status[api] = False
    
    # Mostrar advertencia si no hay APIs configuradas
    if not any(api_status.values()):
        st.error("⚠️ No hay APIs configuradas. Algunas funciones estarán limitadas.")
        st.info("💡 Crea un archivo .env con tus claves API para habilitar todas las funciones.")
    
    st.markdown("---")
    
    # Opciones de investigación
    st.markdown("### 🔍 Opciones de Búsqueda")
    investigation_depth = st.select_slider(
        "Profundidad de investigación",
        options=["Básica", "Estándar", "Profunda"],
        value="Estándar"
    )
    
    include_correlations = st.checkbox("Realizar análisis de correlaciones", value=True)
    generate_report = st.checkbox("Generar reporte PDF automáticamente", value=True)

# Área principal
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Selector de tipo de investigación
    investigation_type = st.selectbox(
        "Selecciona el tipo de investigación",
        ["🌐 Dominio", "📧 Email", "👤 Nombre de Usuario"],
        help="Elige qué tipo de información deseas investigar"
    )
    
    # Mapear tipos a valores internos
    type_mapping = {
        "🌐 Dominio": "domain",
        "📧 Email": "email",
        "👤 Nombre de Usuario": "username"
    }
    
    # Input según el tipo seleccionado
    if investigation_type == "🌐 Dominio":
        target = st.text_input(
            "Ingresa el dominio a investigar",
            placeholder="ejemplo.com",
            help="Ingresa un dominio sin http:// o https://"
        )
    elif investigation_type == "📧 Email":
        target = st.text_input(
            "Ingresa el email a investigar",
            placeholder="usuario@ejemplo.com",
            help="Ingresa una dirección de correo electrónico válida"
        )
    else:  # Nombre de Usuario
        target = st.text_input(
            "Ingresa el nombre de usuario a buscar",
            placeholder="usuario123",
            help="Ingresa el nombre de usuario/alias a buscar en múltiples plataformas"
        )
    
    # Botón de búsqueda
    search_button = st.button("🔍 Iniciar Investigación", type="primary", use_container_width=True)

# Proceso de investigación
if search_button and target:
    with st.spinner("🔄 Realizando investigación... Esto puede tomar varios minutos."):
        try:
            # Obtener tipo interno
            internal_type = type_mapping[investigation_type]
            
            # Crear analizador según el tipo
            if internal_type == "domain":
                analyzer = DomainAnalyzer()
                raw_results = run_async(analyzer.analyze_domain(target))
            elif internal_type == "email":
                investigator = EmailInvestigator()
                raw_results = run_async(investigator.investigate_email(target))
            else:  # username
                searcher = UsernameSearcher()
                raw_results = run_async(searcher.search_username(target))
            
            # Procesar resultados
            processed_results = st.session_state.data_processor.process_investigation_results(
                internal_type, target, raw_results
            )
            
            # Guardar en sesión
            st.session_state.investigations.append(processed_results)
            st.session_state.current_investigation = processed_results
            
            st.success("✅ Investigación completada exitosamente!")
            
        except Exception as e:
            st.error(f"❌ Error durante la investigación: {str(e)}")

# Mostrar resultados si existen
if st.session_state.current_investigation:
    results = st.session_state.current_investigation
    
    # Métricas principales
    st.markdown("---")
    st.markdown("### 📊 Resumen de Resultados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Métricas según el tipo de investigación
    inv_type = results.get('_metadata', {}).get('investigation_type')
    
    if inv_type == 'domain':
        with col1:
            st.metric("Subdominios", results.get('total_subdomains', 0))
        with col2:
            emails_count = len(results.get('consolidated_emails', []))
            st.metric("Emails", emails_count)
        with col3:
            security_score = results.get('security_analysis', {}).get('score', 0)
            st.metric("Seguridad", f"{security_score}/100")
        with col4:
            services_count = len(results.get('shodan', {}).get('services', []))
            st.metric("Servicios", services_count)
    
    elif inv_type == 'email':
        with col1:
            breach_count = len(results.get('breaches', []))
            st.metric("Brechas", breach_count, delta_color="inverse")
        with col2:
            risk_level = results.get('risk_assessment', {}).get('level', 'N/A')
            st.metric("Riesgo", risk_level)
        with col3:
            credibility = results.get('credibility_analysis', {}).get('score', 0)
            st.metric("Credibilidad", f"{credibility}/100")
        with col4:
            profiles = len(results.get('social_profiles', []))
            st.metric("Perfiles", profiles)
    
    else:  # username
        with col1:
            found = results.get('profiles_found', 0)
            st.metric("Encontrados", found)
        with col2:
            possible = results.get('profiles_possible', 0)
            st.metric("Posibles", possible)
        with col3:
            total_checked = results.get('total_platforms_checked', 0)
            st.metric("Plataformas", total_checked)
        with col4:
            score = results.get('digital_profile', {}).get('presence_score', 0)
            st.metric("Presencia", f"{score}/100")
    
    # Tabs para diferentes secciones de resultados
    tabs = st.tabs(["📋 Detalles", "📊 Visualizaciones", "🔗 Correlaciones", "📄 Datos Raw"])
    
    with tabs[0]:  # Detalles
        if inv_type == 'domain':
            # Información del dominio
            if results.get('whois'):
                st.markdown("#### 🌐 Información WHOIS")
                whois_data = results['whois']
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Registrador:** {whois_data.get('registrar', 'N/A')}")
                    st.write(f"**Fecha de creación:** {whois_data.get('creation_date', 'N/A')}")
                    st.write(f"**País:** {whois_data.get('country', 'N/A')}")
                with col2:
                    st.write(f"**Organización:** {whois_data.get('org', 'N/A')}")
                    st.write(f"**Fecha de expiración:** {whois_data.get('expiration_date', 'N/A')}")
            
            # Subdominios
            if results.get('subdomains'):
                st.markdown("#### 🔗 Subdominios Encontrados")
                subdomains_df = pd.DataFrame(results['subdomains'], columns=['Subdominio'])
                st.dataframe(subdomains_df, use_container_width=True)
            
            # Tecnologías
            if results.get('technologies'):
                st.markdown("#### 💻 Tecnologías Detectadas")
                tech = results['technologies']
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Servidor:** {tech.get('server', 'N/A')}")
                    st.write(f"**CMS:** {tech.get('cms', 'N/A')}")
                with col2:
                    if tech.get('frameworks'):
                        st.write(f"**Frameworks:** {', '.join(tech['frameworks'])}")
                    if tech.get('analytics'):
                        st.write(f"**Analytics:** {', '.join(tech['analytics'])}")
        
        elif inv_type == 'email':
            # Verificación del email
            if results.get('verification'):
                st.markdown("#### ✉️ Verificación del Email")
                ver = results['verification']
                
                # Crear visualización de estado
                status_cols = st.columns(4)
                with status_cols[0]:
                    if ver.get('domain_exists'):
                        st.success("✅ Dominio válido")
                    else:
                        st.error("❌ Dominio inválido")
                with status_cols[1]:
                    if ver.get('mx_records'):
                        st.success("✅ MX Records")
                    else:
                        st.error("❌ Sin MX Records")
                with status_cols[2]:
                    if not ver.get('disposable'):
                        st.success("✅ No desechable")
                    else:
                        st.warning("⚠️ Email desechable")
                with status_cols[3]:
                    if not ver.get('role_based'):
                        st.success("✅ Personal")
                    else:
                        st.info("ℹ️ Email de rol")
            
            # Brechas de datos
            if results.get('breaches'):
                st.markdown("#### 🚨 Brechas de Datos")
                st.error(f"⚠️ Email encontrado en {len(results['breaches'])} brechas de datos")
                
                breach_data = []
                for breach in results['breaches']:
                    breach_data.append({
                        'Nombre': breach.get('name', 'N/A'),
                        'Fecha': breach.get('date', 'N/A'),
                        'Datos Comprometidos': ', '.join(breach.get('data_classes', []))[:50] + '...'
                    })
                
                breach_df = pd.DataFrame(breach_data)
                st.dataframe(breach_df, use_container_width=True)
        
        else:  # username
            # Perfiles encontrados
            if results.get('found'):
                st.markdown("#### ✅ Perfiles Confirmados")
                
                profile_data = []
                for profile in results['found']:
                    profile_data.append({
                        'Plataforma': profile.get('platform'),
                        'URL': profile.get('url'),
                        'Estado': '✅ Confirmado'
                    })
                
                profile_df = pd.DataFrame(profile_data)
                st.dataframe(profile_df, use_container_width=True)
            
            # Análisis del perfil digital
            if results.get('digital_profile'):
                st.markdown("#### 👤 Análisis del Perfil Digital")
                profile = results['digital_profile']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Score de presencia:** {profile.get('presence_score', 0)}/100")
                    if profile.get('primary_platforms'):
                        st.write(f"**Plataformas principales:** {', '.join(profile['primary_platforms'][:5])}")
                with col2:
                    if profile.get('interests'):
                        st.write(f"**Intereses detectados:** {', '.join(profile['interests'])}")
    
    with tabs[1]:  # Visualizaciones
        if inv_type == 'domain':
            # Gráfico de registros DNS
            if results.get('dns_records'):
                dns_data = []
                for record_type, records in results['dns_records'].items():
                    if records:
                        dns_data.append({'Tipo': record_type, 'Cantidad': len(records)})
                
                if dns_data:
                    dns_df = pd.DataFrame(dns_data)
                    fig = px.bar(dns_df, x='Tipo', y='Cantidad', 
                                title='Registros DNS por Tipo',
                                color='Cantidad',
                                color_continuous_scale='viridis')
                    st.plotly_chart(fig, use_container_width=True)
        
        elif inv_type == 'email':
            # Gráfico de riesgo
            if results.get('risk_assessment'):
                risk = results['risk_assessment']
                score = risk.get('score', 0)
                
                # Gauge chart para el score de riesgo
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Score de Riesgo"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkred" if score > 70 else "orange" if score > 40 else "green"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgreen"},
                            {'range': [40, 70], 'color': "lightyellow"},
                            {'range': [70, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
        
        else:  # username
            # Gráfico de plataformas por categoría
            if results.get('analysis') and results['analysis'].get('platforms_by_category'):
                cat_data = []
                for category, count in results['analysis']['platforms_by_category'].items():
                    cat_data.append({'Categoría': category.replace('_', ' ').title(), 'Cantidad': count})
                
                cat_df = pd.DataFrame(cat_data)
                fig = px.pie(cat_df, values='Cantidad', names='Categoría',
                           title='Distribución de Plataformas por Categoría')
                st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:  # Correlaciones
        if include_correlations and len(st.session_state.investigations) > 1:
            correlations = st.session_state.data_processor.correlate_investigations(
                st.session_state.investigations
            )
            
            st.markdown("#### 🔗 Entidades Comunes")
            if correlations.get('common_entities'):
                for entity, appearances in correlations['common_entities'].items():
                    st.write(f"**{entity}** aparece en {len(appearances)} investigaciones")
            else:
                st.info("No se encontraron entidades comunes entre las investigaciones")
            
            if correlations.get('insights'):
                st.markdown("#### 💡 Insights")
                for insight in correlations['insights']:
                    st.info(insight)
        else:
            st.info("Realiza más investigaciones para ver correlaciones")
    
    with tabs[3]:  # Datos Raw
        st.markdown("#### 📄 Datos Raw (JSON)")
        st.json(results)

# Sección de generación de reportes
if st.session_state.investigations:
    st.markdown("---")
    st.markdown("### 📊 Generar Reporte Consolidado")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("📄 Generar Reporte PDF", use_container_width=True):
            with st.spinner("Generando reporte..."):
                try:
                    # Generar resumen
                    summary = st.session_state.data_processor.generate_summary_report(
                        st.session_state.investigations
                    )
                    
                    # Generar correlaciones si hay múltiples investigaciones
                    correlations = None
                    if len(st.session_state.investigations) > 1:
                        correlations = st.session_state.data_processor.correlate_investigations(
                            st.session_state.investigations
                        )
                    
                    # Generar PDF
                    report_gen = ReportGenerator()
                    pdf_bytes = report_gen.generate_pdf_report(
                        st.session_state.investigations,
                        summary,
                        correlations
                    )
                    
                    # Ofrecer descarga
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"OSINT_NEXUS_Report_{timestamp}.pdf"
                    
                    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}">📥 Descargar Reporte PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                    st.success("✅ Reporte generado exitosamente!")
                    
                except Exception as e:
                    st.error(f"Error generando el reporte: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <p>OSINT-NEXUS v1.0 | Desarrollado con ❤️ para investigaciones éticas</p>
        <p style="font-size: 0.8rem;">⚠️ Usa esta herramienta de manera responsable y legal</p>
    </div>
    """,
    unsafe_allow_html=True
)