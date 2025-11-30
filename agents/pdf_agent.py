# agents/pdf_agent.py
from fpdf import FPDF
import os
import tempfile
import textwrap

class PDFReport:
    def __init__(self, title="Research Report"):
        self.title = title
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def add_markdown(self, md_text):
        # very simple markdown to PDF conversion (headlines and paragraphs)
        lines = md_text.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                self.pdf.ln(4)
                continue
            if line.startswith("# "):
                self.pdf.set_font("Arial", "B", 16)
                self.pdf.cell(0, 8, line[2:], ln=True)
            elif line.startswith("## "):
                self.pdf.set_font("Arial", "B", 13)
                self.pdf.multi_cell(0, 7, line[3:])
            elif line.startswith("- "):
                self.pdf.set_font("Arial", "", 11)
                self.pdf.multi_cell(0, 6, "• " + line[2:])
            else:
                self.pdf.set_font("Arial", "", 11)
                # wrap
                self.pdf.multi_cell(0, 6, line)
        self.pdf.ln(6)

    def save(self, filename=None):
        if not filename:
            fd, filename = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
        self.pdf.output(filename)
        return filename
