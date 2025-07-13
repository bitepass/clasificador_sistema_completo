from fpdf import FPDF
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class PDFReport(FPDF):
    def header(self):
        # Title
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "OSINT-Nexus Informe de Inteligencia", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")


def generate_pdf(target_type: str, target_value: str, data: Dict[str, Any], output_path: Path) -> Path:
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.utcnow().isoformat()} UTC", ln=True)
    pdf.cell(0, 10, f"Tipo de objetivo: {target_type}", ln=True)
    pdf.cell(0, 10, f"Valor introducido: {target_value}", ln=True)
    pdf.ln(5)

    for section, content in data.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, section, ln=True)
        pdf.set_font("Arial", size=11)
        if isinstance(content, dict):
            for k, v in content.items():
                pdf.multi_cell(0, 7, f"- {k}: {v}")
        elif isinstance(content, list):
            for item in content:
                pdf.multi_cell(0, 7, f"- {item}")
        else:
            pdf.multi_cell(0, 7, str(content))
        pdf.ln(3)

    output_path = output_path.expanduser().resolve()
    pdf.output(str(output_path))
    return output_path