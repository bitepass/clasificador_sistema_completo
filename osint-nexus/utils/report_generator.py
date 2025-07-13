"""
Generador de Reportes PDF para OSINT-Nexus
Crea reportes profesionales con los resultados de las investigaciones
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import io
import base64

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generador de reportes PDF profesionales"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Crear estilos personalizados para el reporte"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Estilo para texto de riesgo alto
        self.styles.add(ParagraphStyle(
            name='HighRisk',
            parent=self.styles['Normal'],
            textColor=colors.HexColor('#e74c3c'),
            fontSize=11,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para texto de éxito
        self.styles.add(ParagraphStyle(
            name='Success',
            parent=self.styles['Normal'],
            textColor=colors.HexColor('#27ae60'),
            fontSize=11
        ))
        
    def generate_pdf_report(self, investigations: List[Dict[str, Any]], 
                          summary: Dict[str, Any],
                          correlations: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Generar reporte PDF completo
        
        Args:
            investigations: Lista de investigaciones realizadas
            summary: Resumen ejecutivo
            correlations: Correlaciones encontradas (opcional)
            
        Returns:
            Bytes del PDF generado
        """
        # Crear buffer para el PDF
        buffer = io.BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Construir contenido
        story = []
        
        # Página de título
        story.extend(self._create_title_page())
        story.append(PageBreak())
        
        # Resumen ejecutivo
        story.extend(self._create_executive_summary(summary))
        story.append(PageBreak())
        
        # Detalle de investigaciones
        for idx, investigation in enumerate(investigations):
            story.extend(self._create_investigation_section(investigation, idx + 1))
            if idx < len(investigations) - 1:
                story.append(PageBreak())
        
        # Correlaciones si existen
        if correlations:
            story.append(PageBreak())
            story.extend(self._create_correlations_section(correlations))
        
        # Recomendaciones
        story.append(PageBreak())
        story.extend(self._create_recommendations_section(summary))
        
        # Construir PDF
        doc.build(story, onFirstPage=self._add_header_footer, 
                 onLaterPages=self._add_header_footer)
        
        # Obtener bytes del PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_title_page(self) -> List:
        """Crear página de título"""
        elements = []
        
        # Logo/Título
        elements.append(Spacer(1, 2*inch))
        title = Paragraph("OSINT-NEXUS", self.styles['CustomTitle'])
        elements.append(title)
        
        subtitle = Paragraph("Reporte de Inteligencia de Fuentes Abiertas", 
                           self.styles['Heading2'])
        elements.append(subtitle)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Información del reporte
        date_str = datetime.now().strftime("%d de %B de %Y")
        info_text = f"""
        <para align="center">
        <b>Fecha de Generación:</b> {date_str}<br/>
        <b>Clasificación:</b> Confidencial<br/>
        <b>Versión:</b> 1.0
        </para>
        """
        elements.append(Paragraph(info_text, self.styles['Normal']))
        
        elements.append(Spacer(1, 2*inch))
        
        # Disclaimer
        disclaimer = """
        <para align="center">
        <font size="9">
        Este reporte contiene información recopilada de fuentes públicas disponibles.
        La información presentada debe ser verificada de forma independiente antes de
        tomar cualquier acción basada en estos hallazgos.
        </font>
        </para>
        """
        elements.append(Paragraph(disclaimer, self.styles['Normal']))
        
        return elements
    
    def _create_executive_summary(self, summary: Dict[str, Any]) -> List:
        """Crear sección de resumen ejecutivo"""
        elements = []
        
        elements.append(Paragraph("Resumen Ejecutivo", self.styles['CustomHeading']))
        
        # Estadísticas generales
        stats_data = [
            ['Métrica', 'Valor'],
            ['Total de Investigaciones', str(summary.get('total_investigations', 0))],
            ['Entidades Descubiertas', str(summary.get('total_entities_discovered', 0))],
            ['Hallazgos de Alto Riesgo', str(len(summary.get('risk_summary', {}).get('high_risk_findings', [])))]
        ]
        
        # Agregar tipos de investigación
        for inv_type, count in summary.get('investigation_types', {}).items():
            stats_data.append([f'Investigaciones de {inv_type.title()}', str(count)])
        
        # Crear tabla
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Hallazgos clave
        if summary.get('key_findings'):
            elements.append(Paragraph("Hallazgos Clave:", self.styles['Heading3']))
            for finding in summary['key_findings'][:5]:  # Top 5 hallazgos
                elements.append(Paragraph(f"• {finding}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_investigation_section(self, investigation: Dict[str, Any], 
                                    index: int) -> List:
        """Crear sección para una investigación individual"""
        elements = []
        
        inv_type = investigation.get('_metadata', {}).get('investigation_type', 'Unknown')
        target = investigation.get('_metadata', {}).get('target', 'Unknown')
        
        elements.append(Paragraph(f"Investigación {index}: {inv_type.title()}", 
                                self.styles['CustomHeading']))
        elements.append(Paragraph(f"<b>Objetivo:</b> {target}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Contenido específico según el tipo
        if inv_type == 'domain':
            elements.extend(self._create_domain_investigation_content(investigation))
        elif inv_type == 'email':
            elements.extend(self._create_email_investigation_content(investigation))
        elif inv_type == 'username':
            elements.extend(self._create_username_investigation_content(investigation))
        
        return elements
    
    def _create_domain_investigation_content(self, investigation: Dict[str, Any]) -> List:
        """Contenido específico para investigación de dominio"""
        elements = []
        
        # Información básica
        if investigation.get('ip_info'):
            ip_info = investigation['ip_info']
            elements.append(Paragraph("<b>Información de IP:</b>", self.styles['Heading4']))
            elements.append(Paragraph(f"IP: {ip_info.get('ip', 'N/A')}", self.styles['Normal']))
            elements.append(Paragraph(f"ASN: {ip_info.get('asn', 'N/A')}", self.styles['Normal']))
            elements.append(Paragraph(f"País: {ip_info.get('asn_country', 'N/A')}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Subdominios
        if investigation.get('subdomains'):
            elements.append(Paragraph("<b>Subdominios Encontrados:</b>", self.styles['Heading4']))
            subdomain_list = investigation['subdomains'][:10]  # Primeros 10
            for subdomain in subdomain_list:
                elements.append(Paragraph(f"• {subdomain}", self.styles['Normal']))
            if len(investigation['subdomains']) > 10:
                elements.append(Paragraph(f"... y {len(investigation['subdomains']) - 10} más", 
                                        self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Análisis de seguridad
        if investigation.get('security_analysis'):
            sec_analysis = investigation['security_analysis']
            score = sec_analysis.get('score', 0)
            
            elements.append(Paragraph("<b>Análisis de Seguridad:</b>", self.styles['Heading4']))
            
            # Color según el score
            if score >= 80:
                style = self.styles['Success']
            elif score >= 50:
                style = self.styles['Normal']
            else:
                style = self.styles['HighRisk']
            
            elements.append(Paragraph(f"Puntuación de Seguridad: {score}/100", style))
            
            if sec_analysis.get('issues'):
                for issue in sec_analysis['issues']:
                    elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
        
        return elements
    
    def _create_email_investigation_content(self, investigation: Dict[str, Any]) -> List:
        """Contenido específico para investigación de email"""
        elements = []
        
        # Verificación
        if investigation.get('verification'):
            ver = investigation['verification']
            elements.append(Paragraph("<b>Verificación de Email:</b>", self.styles['Heading4']))
            
            ver_data = [
                ['Propiedad', 'Estado'],
                ['Dominio Existe', '✓' if ver.get('domain_exists') else '✗'],
                ['Registros MX', '✓' if ver.get('mx_records') else '✗'],
                ['Email Desechable', '✗' if not ver.get('disposable') else '✓'],
                ['Email de Rol', '✗' if not ver.get('role_based') else '✓']
            ]
            
            ver_table = Table(ver_data, colWidths=[2*inch, 1*inch])
            ver_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))
            
            elements.append(ver_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Brechas de datos
        if investigation.get('breaches'):
            elements.append(Paragraph("<b>Brechas de Datos:</b>", self.styles['Heading4']))
            elements.append(Paragraph(f"Email encontrado en {len(investigation['breaches'])} brechas:", 
                                    self.styles['HighRisk']))
            
            for breach in investigation['breaches'][:5]:  # Primeras 5 brechas
                breach_text = f"• <b>{breach.get('name', 'Unknown')}</b> - {breach.get('date', 'Fecha desconocida')}"
                if breach.get('data_classes'):
                    breach_text += f" (Datos expuestos: {', '.join(breach['data_classes'][:3])})"
                elements.append(Paragraph(breach_text, self.styles['Normal']))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Análisis de riesgo
        if investigation.get('risk_assessment'):
            risk = investigation['risk_assessment']
            level = risk.get('level', 'DESCONOCIDO')
            
            style_map = {
                'ALTO': self.styles['HighRisk'],
                'MEDIO': self.styles['Normal'],
                'BAJO': self.styles['Success']
            }
            
            elements.append(Paragraph(f"<b>Nivel de Riesgo:</b> {level}", 
                                    style_map.get(level, self.styles['Normal'])))
            
            if risk.get('factors'):
                elements.append(Paragraph("Factores de riesgo:", self.styles['Normal']))
                for factor in risk['factors']:
                    elements.append(Paragraph(f"• {factor}", self.styles['Normal']))
        
        return elements
    
    def _create_username_investigation_content(self, investigation: Dict[str, Any]) -> List:
        """Contenido específico para investigación de username"""
        elements = []
        
        # Resumen de perfiles
        elements.append(Paragraph("<b>Resumen de Búsqueda:</b>", self.styles['Heading4']))
        elements.append(Paragraph(f"Plataformas verificadas: {investigation.get('total_platforms_checked', 0)}", 
                                self.styles['Normal']))
        elements.append(Paragraph(f"Perfiles encontrados: {investigation.get('profiles_found', 0)}", 
                                self.styles['Success']))
        elements.append(Paragraph(f"Perfiles posibles: {investigation.get('profiles_possible', 0)}", 
                                self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Perfiles encontrados
        if investigation.get('found'):
            elements.append(Paragraph("<b>Perfiles Confirmados:</b>", self.styles['Heading4']))
            
            profile_data = [['Plataforma', 'URL']]
            for profile in investigation['found'][:10]:  # Primeros 10
                profile_data.append([
                    profile.get('platform', 'Unknown'),
                    profile.get('url', 'N/A')[:50] + '...' if len(profile.get('url', '')) > 50 else profile.get('url', 'N/A')
                ])
            
            profile_table = Table(profile_data, colWidths=[1.5*inch, 4*inch])
            profile_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))
            
            elements.append(profile_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Análisis de perfil digital
        if investigation.get('digital_profile'):
            profile = investigation['digital_profile']
            elements.append(Paragraph("<b>Análisis de Perfil Digital:</b>", self.styles['Heading4']))
            elements.append(Paragraph(f"Puntuación de presencia: {profile.get('presence_score', 0)}/100", 
                                    self.styles['Normal']))
            
            if profile.get('interests'):
                elements.append(Paragraph("Intereses detectados:", self.styles['Normal']))
                for interest in profile['interests']:
                    elements.append(Paragraph(f"• {interest.replace('_', ' ').title()}", 
                                            self.styles['Normal']))
        
        return elements
    
    def _create_correlations_section(self, correlations: Dict[str, Any]) -> List:
        """Crear sección de correlaciones"""
        elements = []
        
        elements.append(Paragraph("Análisis de Correlaciones", self.styles['CustomHeading']))
        
        # Insights
        if correlations.get('insights'):
            elements.append(Paragraph("<b>Insights Descubiertos:</b>", self.styles['Heading4']))
            for insight in correlations['insights']:
                elements.append(Paragraph(f"• {insight}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Entidades comunes
        if correlations.get('common_entities'):
            elements.append(Paragraph("<b>Entidades Comunes:</b>", self.styles['Heading4']))
            
            common_data = [['Entidad', 'Apariciones']]
            for entity, appearances in list(correlations['common_entities'].items())[:10]:
                common_data.append([
                    entity[:40] + '...' if len(entity) > 40 else entity,
                    str(len(appearances))
                ])
            
            common_table = Table(common_data, colWidths=[4*inch, 1.5*inch])
            common_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))
            
            elements.append(common_table)
        
        return elements
    
    def _create_recommendations_section(self, summary: Dict[str, Any]) -> List:
        """Crear sección de recomendaciones"""
        elements = []
        
        elements.append(Paragraph("Recomendaciones", self.styles['CustomHeading']))
        
        if summary.get('recommendations'):
            for idx, recommendation in enumerate(summary['recommendations'], 1):
                elements.append(Paragraph(f"{idx}. {recommendation}", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        else:
            elements.append(Paragraph("No hay recomendaciones específicas en este momento.", 
                                    self.styles['Normal']))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Nota final
        final_note = """
        <para align="justify">
        <font size="10">
        <b>Nota Importante:</b> Este reporte se basa en información disponible públicamente
        en el momento de la investigación. La situación puede cambiar rápidamente, por lo que
        se recomienda realizar investigaciones periódicas para mantener la información actualizada.
        Todas las acciones tomadas basándose en este reporte deben cumplir con las leyes y
        regulaciones aplicables.
        </font>
        </para>
        """
        elements.append(Paragraph(final_note, self.styles['Normal']))
        
        return elements
    
    def _add_header_footer(self, canvas, doc):
        """Agregar encabezado y pie de página a cada página"""
        canvas.saveState()
        
        # Encabezado
        canvas.setFont('Helvetica', 9)
        canvas.drawString(inch, 10.5*inch, "OSINT-NEXUS - Reporte Confidencial")
        canvas.drawRightString(7.5*inch, 10.5*inch, 
                              datetime.now().strftime("%d/%m/%Y"))
        
        # Línea separadora
        canvas.setStrokeColor(colors.grey)
        canvas.line(inch, 10.3*inch, 7.5*inch, 10.3*inch)
        
        # Pie de página
        canvas.setFont('Helvetica', 8)
        canvas.drawString(inch, 0.75*inch, 
                         "© 2024 OSINT-NEXUS - Información Confidencial")
        canvas.drawRightString(7.5*inch, 0.75*inch, 
                              f"Página {doc.page}")
        
        canvas.restoreState()