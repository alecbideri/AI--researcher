from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import os

def generate_pdf_report(content: str, filename: str = "report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story = []
    
    # Title
    Story.append(Paragraph("AI Research Report", styles["Title"]))
    Story.append(Spacer(1, 12))

    # Content - Handle basic markdown-like newlines
    # ReportLab Paragraphs handle text wrapping automatically.
    # We'll split by double newlines to create separate paragraphs.
    paragraphs = content.split('\n\n')
    
    for p_text in paragraphs:
        # Replace single newlines with spaces to let ReportLab handle wrapping, 
        # unless it's a list item or specific formatting is needed.
        # For simple text, this is often enough.
        # We can also support basic bolding if we parse **text** to <b>text</b>
        formatted_text = p_text.replace('\n', '<br/>')
        
        # Basic Bold parsing (very simple)
        formatted_text = formatted_text.replace('**', '<b>', 1).replace('**', '</b>', 1)
        
        Story.append(Paragraph(formatted_text, styles["Normal"]))
        Story.append(Spacer(1, 12))

    doc.build(Story)
    return os.path.abspath(filename)
