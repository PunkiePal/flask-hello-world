import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#777777"))
        
        # Draw dynamic page footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        
        # Optional: Add your license watermark dynamically at the bottom edge
        license_text = "Zero Access Framework - Individual Developer License"
        self.drawString(54, 36, license_text)
        self.restoreState()

def create_manual(pdf_filename, customer_name="Valued Customer", license_key="DEMO-LICENSE"):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette Styles
    title_style = ParagraphStyle(
        'ManualTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A2B4C"),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'ManualBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#333333"),
        spaceAfter=10
    )

    story = []
    
    # Title Page Content
    story.append(Spacer(1, 100))
    story.append(Paragraph("Security & Technical Manual Generator", title_style))
    story.append(Paragraph("Documentation Framework for Single User Deployments", styles['Heading3']))
    story.append(Spacer(1, 40))
    
    # Dynamic Licensing Attribution Box
    license_html = f"<b>Licensed To:</b> {customer_name}<br/><b>License Type:</b> Individual Developer License<br/><b>Key:</b> {license_key}"
    story.append(Paragraph(license_html, body_style))
    story.append(PageBreak())
    
    # Core Document Placeholder Content
    story.append(Paragraph("1. Technical Architecture Summary", styles['Heading2']))
    story.append(Paragraph("This document provides standard operating procedures, architectural topology profiles, and programmatic blueprints for system components operating under zero-access constraints.", body_style))
    
    # Build document via our dual-pass layout canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully with size {os.path.getsize(pdf_filename)} bytes")

if __name__ == "__main__":
    create_manual("test_output.pdf")

