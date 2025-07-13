"""
Generador de reportes para OSINT-Nexus
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import csv
import xml.etree.ElementTree as ET

class ReportGenerator:
    """Generador de reportes en múltiples formatos"""
    
    def __init__(self, results: Dict[str, Any], investigation_type: str):
        """
        Inicializa el generador de reportes
        
        Args:
            results: Resultados de la investigación
            investigation_type: Tipo de investigación realizada
        """
        self.results = results
        self.investigation_type = investigation_type
        self.timestamp = datetime.now()
        
    def generate_json_report(self) -> str:
        """
        Genera un reporte en formato JSON
        
        Returns:
            JSON string con el reporte
        """
        report = {
            "metadata": {
                "tool": "OSINT-Nexus",
                "version": "1.0.0",
                "timestamp": self.timestamp.isoformat(),
                "investigation_type": self.investigation_type,
                "target": self._get_target_from_results()
            },
            "results": self.results,
            "summary": self._generate_summary()
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def generate_csv_report(self) -> str:
        """
        Genera un reporte en formato CSV
        
        Returns:
            CSV string con el reporte
        """
        if self.investigation_type == "username":
            return self._generate_username_csv()
        elif self.investigation_type == "domain":
            return self._generate_domain_csv()
        elif self.investigation_type == "email":
            return self._generate_email_csv()
        elif self.investigation_type == "url":
            return self._generate_social_csv()
        else:
            return self._generate_generic_csv()
    
    def generate_xml_report(self) -> str:
        """
        Genera un reporte en formato XML
        
        Returns:
            XML string con el reporte
        """
        root = ET.Element("osint_report")
        
        # Metadata
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "tool").text = "OSINT-Nexus"
        ET.SubElement(metadata, "version").text = "1.0.0"
        ET.SubElement(metadata, "timestamp").text = self.timestamp.isoformat()
        ET.SubElement(metadata, "investigation_type").text = self.investigation_type
        ET.SubElement(metadata, "target").text = self._get_target_from_results()
        
        # Results
        results_elem = ET.SubElement(root, "results")
        self._dict_to_xml(self.results, results_elem)
        
        # Summary
        summary_elem = ET.SubElement(root, "summary")
        summary_data = self._generate_summary()
        self._dict_to_xml(summary_data, summary_elem)
        
        return ET.tostring(root, encoding='unicode')
    
    def generate_html_report(self) -> str:
        """
        Genera un reporte en formato HTML
        
        Returns:
            HTML string con el reporte
        """
        target = self._get_target_from_results()
        summary = self._generate_summary()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OSINT-Nexus Report - {target}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #007bff;
                    margin: 0;
                }}
                .metadata {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .section h2 {{
                    color: #333;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 10px;
                }}
                .metric {{
                    display: inline-block;
                    background-color: #e9ecef;
                    padding: 10px 15px;
                    margin: 5px;
                    border-radius: 5px;
                    border-left: 4px solid #007bff;
                }}
                .metric-label {{
                    font-weight: bold;
                    color: #495057;
                }}
                .metric-value {{
                    color: #007bff;
                    font-size: 1.2em;
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                .table th, .table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .table th {{
                    background-color: #007bff;
                    color: white;
                }}
                .table tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                .success {{
                    color: #28a745;
                    font-weight: bold;
                }}
                .error {{
                    color: #dc3545;
                    font-weight: bold;
                }}
                .warning {{
                    color: #ffc107;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #6c757d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 OSINT-Nexus Report</h1>
                    <p>Reporte de Investigación - {self.investigation_type.upper()}</p>
                </div>
                
                <div class="metadata">
                    <h2>📋 Información General</h2>
                    <div class="metric">
                        <span class="metric-label">Objetivo:</span>
                        <span class="metric-value">{target}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Tipo:</span>
                        <span class="metric-value">{self.investigation_type.upper()}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Fecha:</span>
                        <span class="metric-value">{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Herramienta:</span>
                        <span class="metric-value">OSINT-Nexus v1.0.0</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Resumen de Resultados</h2>
                    {self._generate_summary_html(summary)}
                </div>
                
                <div class="section">
                    <h2>🔍 Resultados Detallados</h2>
                    {self._generate_detailed_html()}
                </div>
                
                <div class="footer">
                    <p>Generado por <strong>OSINT-Nexus v1.0.0</strong> - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Este reporte contiene información obtenida de fuentes públicas para fines de investigación legítima.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def save_report(self, format: str, filename: str = None) -> str:
        """
        Guarda el reporte en el formato especificado
        
        Args:
            format: Formato del reporte (json, csv, xml, html)
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del archivo guardado
        """
        if not filename:
            target = self._get_target_from_results()
            safe_target = "".join(c for c in target if c.isalnum() or c in ('-', '_'))
            timestamp = self.timestamp.strftime('%Y%m%d_%H%M%S')
            filename = f"osint_report_{self.investigation_type}_{safe_target}_{timestamp}.{format}"
        
        # Crear directorio de reportes si no existe
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        filepath = reports_dir / filename
        
        if format.lower() == 'json':
            content = self.generate_json_report()
        elif format.lower() == 'csv':
            content = self.generate_csv_report()
        elif format.lower() == 'xml':
            content = self.generate_xml_report()
        elif format.lower() == 'html':
            content = self.generate_html_report()
        else:
            raise ValueError(f"Formato no soportado: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def _get_target_from_results(self) -> str:
        """Extrae el objetivo de los resultados"""
        target_keys = ['domain', 'email', 'username', 'profile_url']
        
        for key in target_keys:
            if key in self.results:
                return str(self.results[key])
        
        return "Unknown"
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Genera un resumen de los resultados"""
        summary = {
            "target": self._get_target_from_results(),
            "investigation_type": self.investigation_type,
            "timestamp": self.timestamp.isoformat(),
            "status": "completed"
        }
        
        if self.investigation_type == "domain":
            basic_info = self.results.get('basic_info', {})
            summary.update({
                "domain_active": basic_info.get('is_active', False),
                "ip_address": basic_info.get('ip_address', 'N/A'),
                "subdomains_found": len(self.results.get('subdomains', [])),
                "security_rating": self.results.get('security_headers', {}).get('rating', 'Unknown')
            })
        
        elif self.investigation_type == "email":
            validation = self.results.get('validation', {})
            breaches = self.results.get('breaches', {})
            summary.update({
                "format_valid": validation.get('format_valid', False),
                "domain_exists": validation.get('domain_exists', False),
                "found_in_breaches": breaches.get('found_in_breaches', False),
                "breach_count": breaches.get('breach_count', 0)
            })
        
        elif self.investigation_type == "username":
            stats = self.results.get('statistics', {})
            summary.update({
                "platforms_checked": stats.get('total_platforms_checked', 0),
                "platforms_found": stats.get('platforms_found', 0),
                "availability_score": stats.get('presence_percentage', 0)
            })
        
        elif self.investigation_type == "url":
            basic_info = self.results.get('basic_info', {})
            platform_analysis = self.results.get('platform_analysis', {})
            summary.update({
                "platform": self.results.get('platform', 'Unknown'),
                "accessible": basic_info.get('accessible', False),
                "verified": platform_analysis.get('verified', False)
            })
        
        return summary
    
    def _generate_username_csv(self) -> str:
        """Genera CSV específico para análisis de username"""
        output = []
        output.append("Platform,Status,URL,Additional_Info,Last_Checked")
        
        platform_results = self.results.get('platform_results', [])
        for result in platform_results:
            status = "Found" if result.get('exists') else "Not Found"
            additional_info = json.dumps(result.get('additional_info', {}))
            
            output.append(f"{result.get('platform', 'N/A')},{status},{result.get('url', 'N/A')},{additional_info},{result.get('last_checked', 'N/A')}")
        
        return '\n'.join(output)
    
    def _generate_domain_csv(self) -> str:
        """Genera CSV específico para análisis de dominio"""
        output = []
        output.append("Domain,IP_Address,Active,Registrar,Creation_Date,Expiration_Date,Security_Rating")
        
        basic_info = self.results.get('basic_info', {})
        whois_info = self.results.get('whois_info', {})
        security = self.results.get('security_headers', {})
        
        output.append(f"{self.results.get('domain', 'N/A')},{basic_info.get('ip_address', 'N/A')},{basic_info.get('is_active', False)},{whois_info.get('registrar', 'N/A')},{whois_info.get('creation_date', 'N/A')},{whois_info.get('expiration_date', 'N/A')},{security.get('rating', 'N/A')}")
        
        return '\n'.join(output)
    
    def _generate_email_csv(self) -> str:
        """Genera CSV específico para análisis de email"""
        output = []
        output.append("Email,Format_Valid,Domain_Exists,Found_in_Breaches,Breach_Count,Trust_Score")
        
        validation = self.results.get('validation', {})
        breaches = self.results.get('breaches', {})
        reputation = self.results.get('reputation', {})
        
        output.append(f"{self.results.get('email', 'N/A')},{validation.get('format_valid', False)},{validation.get('domain_exists', False)},{breaches.get('found_in_breaches', False)},{breaches.get('breach_count', 0)},{reputation.get('trust_score', 0)}")
        
        return '\n'.join(output)
    
    def _generate_social_csv(self) -> str:
        """Genera CSV específico para análisis de redes sociales"""
        output = []
        output.append("Profile_URL,Platform,Accessible,Verified,Followers,Following,Posts")
        
        basic_info = self.results.get('basic_info', {})
        platform_analysis = self.results.get('platform_analysis', {})
        
        output.append(f"{self.results.get('profile_url', 'N/A')},{self.results.get('platform', 'N/A')},{basic_info.get('accessible', False)},{platform_analysis.get('verified', False)},{platform_analysis.get('followers_count', 'N/A')},{platform_analysis.get('following_count', 'N/A')},{platform_analysis.get('posts_count', 'N/A')}")
        
        return '\n'.join(output)
    
    def _generate_generic_csv(self) -> str:
        """Genera CSV genérico"""
        output = []
        output.append("Key,Value")
        
        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, json.dumps(v)))
                else:
                    items.append((new_key, str(v)))
            return dict(items)
        
        flat_results = flatten_dict(self.results)
        for key, value in flat_results.items():
            output.append(f"{key},{value}")
        
        return '\n'.join(output)
    
    def _dict_to_xml(self, data: Dict[str, Any], parent: ET.Element):
        """Convierte diccionario a elementos XML"""
        for key, value in data.items():
            # Limpiar el nombre del elemento
            clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', str(key))
            
            if isinstance(value, dict):
                elem = ET.SubElement(parent, clean_key)
                self._dict_to_xml(value, elem)
            elif isinstance(value, list):
                elem = ET.SubElement(parent, clean_key)
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        item_elem = ET.SubElement(elem, f"item_{i}")
                        self._dict_to_xml(item, item_elem)
                    else:
                        item_elem = ET.SubElement(elem, f"item_{i}")
                        item_elem.text = str(item)
            else:
                elem = ET.SubElement(parent, clean_key)
                elem.text = str(value)
    
    def _generate_summary_html(self, summary: Dict[str, Any]) -> str:
        """Genera HTML para el resumen"""
        html = '<div class="summary-metrics">'
        
        for key, value in summary.items():
            if key not in ['target', 'investigation_type', 'timestamp', 'status']:
                html += f'''
                <div class="metric">
                    <span class="metric-label">{key.replace('_', ' ').title()}:</span>
                    <span class="metric-value">{value}</span>
                </div>
                '''
        
        html += '</div>'
        return html
    
    def _generate_detailed_html(self) -> str:
        """Genera HTML para los resultados detallados"""
        html = '<div class="detailed-results">'
        
        if self.investigation_type == "username":
            html += self._generate_username_html()
        elif self.investigation_type == "domain":
            html += self._generate_domain_html()
        elif self.investigation_type == "email":
            html += self._generate_email_html()
        elif self.investigation_type == "url":
            html += self._generate_social_html()
        
        html += '</div>'
        return html
    
    def _generate_username_html(self) -> str:
        """Genera HTML específico para resultados de username"""
        html = '<table class="table">'
        html += '<tr><th>Plataforma</th><th>Estado</th><th>URL</th><th>Información Adicional</th></tr>'
        
        platform_results = self.results.get('platform_results', [])
        for result in platform_results:
            status = '<span class="success">✓ Encontrado</span>' if result.get('exists') else '<span class="error">✗ No encontrado</span>'
            url = result.get('url', 'N/A')
            additional_info = result.get('additional_info', {})
            
            html += f'''
            <tr>
                <td>{result.get('platform', 'N/A')}</td>
                <td>{status}</td>
                <td><a href="{url}" target="_blank">{url}</a></td>
                <td>{json.dumps(additional_info, indent=2) if additional_info else 'N/A'}</td>
            </tr>
            '''
        
        html += '</table>'
        return html
    
    def _generate_domain_html(self) -> str:
        """Genera HTML específico para resultados de dominio"""
        html = '<h3>Información Básica</h3>'
        
        basic_info = self.results.get('basic_info', {})
        html += f'''
        <div class="metric">
            <span class="metric-label">Estado:</span>
            <span class="metric-value {'success' if basic_info.get('is_active') else 'error'}">{
                '✓ Activo' if basic_info.get('is_active') else '✗ Inactivo'
            }</span>
        </div>
        <div class="metric">
            <span class="metric-label">IP:</span>
            <span class="metric-value">{basic_info.get('ip_address', 'N/A')}</span>
        </div>
        '''
        
        # Información WHOIS
        whois_info = self.results.get('whois_info', {})
        if 'error' not in whois_info:
            html += '<h3>Información WHOIS</h3>'
            html += f'''
            <div class="metric">
                <span class="metric-label">Registrador:</span>
                <span class="metric-value">{whois_info.get('registrar', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Fecha de Creación:</span>
                <span class="metric-value">{whois_info.get('creation_date', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Fecha de Expiración:</span>
                <span class="metric-value">{whois_info.get('expiration_date', 'N/A')}</span>
            </div>
            '''
        
        return html
    
    def _generate_email_html(self) -> str:
        """Genera HTML específico para resultados de email"""
        html = '<h3>Validación</h3>'
        
        validation = self.results.get('validation', {})
        html += f'''
        <div class="metric">
            <span class="metric-label">Formato:</span>
            <span class="metric-value {'success' if validation.get('format_valid') else 'error'}">{
                '✓ Válido' if validation.get('format_valid') else '✗ Inválido'
            }</span>
        </div>
        <div class="metric">
            <span class="metric-label">Dominio:</span>
            <span class="metric-value {'success' if validation.get('domain_exists') else 'error'}">{
                '✓ Existe' if validation.get('domain_exists') else '✗ No existe'
            }</span>
        </div>
        '''
        
        # Información de brechas
        breaches = self.results.get('breaches', {})
        if 'error' not in breaches:
            html += '<h3>Análisis de Brechas</h3>'
            breach_count = breaches.get('breach_count', 0)
            html += f'''
            <div class="metric">
                <span class="metric-label">Brechas encontradas:</span>
                <span class="metric-value {'error' if breach_count > 0 else 'success'}">{breach_count}</span>
            </div>
            '''
        
        return html
    
    def _generate_social_html(self) -> str:
        """Genera HTML específico para resultados de redes sociales"""
        html = '<h3>Información del Perfil</h3>'
        
        platform_analysis = self.results.get('platform_analysis', {})
        if 'error' not in platform_analysis:
            html += f'''
            <div class="metric">
                <span class="metric-label">Nombre:</span>
                <span class="metric-value">{platform_analysis.get('name', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Username:</span>
                <span class="metric-value">{platform_analysis.get('username', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Verificado:</span>
                <span class="metric-value {'success' if platform_analysis.get('verified') else 'error'}">{
                    '✓ Verificado' if platform_analysis.get('verified') else '✗ No verificado'
                }</span>
            </div>
            '''
        
        return html