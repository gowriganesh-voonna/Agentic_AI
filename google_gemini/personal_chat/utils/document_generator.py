import os
import tempfile
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


def create_txt_file(content: str, filename: str = None) -> str:
    """Create a .txt file with the given content."""
    if filename is None:
        filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ TXT file created: {filepath}")
    return filepath


def create_docx_file(content: str, title: str = "Generated Document", filename: str = None) -> str:
    """Create a .docx file with formatted content."""
    if filename is None:
        filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    doc = Document()
    
    # Add title
    heading = doc.add_heading(title, level=0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add timestamp
    timestamp = doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    timestamp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    timestamp.runs[0].font.size = Pt(9)
    timestamp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
    
    doc.add_paragraph()  # Blank line
    
    # Process content - handle sections and formatting
    sections = content.split('\n\n')
    
    for section in sections:
        if section.strip():
            # Check if it's a heading (starts with #, ##, etc.)
            if section.startswith('# '):
                doc.add_heading(section[2:].strip(), level=1)
            elif section.startswith('## '):
                doc.add_heading(section[3:].strip(), level=2)
            elif section.startswith('### '):
                doc.add_heading(section[4:].strip(), level=3)
            # Check if it's a code block (starts with ```)
            elif section.startswith('```'):
                code_content = section.replace('```', '').strip()
                p = doc.add_paragraph(code_content)
                p.style = 'Intense Quote'
            # Regular paragraph
            else:
                # Handle bullet points
                if section.strip().startswith('- ') or section.strip().startswith('* '):
                    for line in section.split('\n'):
                        if line.strip().startswith(('- ', '* ')):
                            doc.add_paragraph(line.strip()[2:], style='List Bullet')
                        elif line.strip():
                            doc.add_paragraph(line.strip())
                # Handle numbered lists
                elif any(section.strip().startswith(f'{i}.') for i in range(1, 10)):
                    for line in section.split('\n'):
                        if line.strip() and line.strip()[0].isdigit():
                            doc.add_paragraph(line.strip().split('.', 1)[1].strip(), style='List Number')
                        elif line.strip():
                            doc.add_paragraph(line.strip())
                else:
                    doc.add_paragraph(section.strip())
    
    doc.save(filepath)
    print(f"✅ DOCX file created: {filepath}")
    return filepath


def create_pdf_file(content: str, title: str = "Generated Document", filename: str = None) -> str:
    """Create a .pdf file with formatted content."""
    if filename is None:
        filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#34495E',
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Build document
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add timestamp
    timestamp = f"<para align='right'><font size=8 color='gray'>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</font></para>"
    story.append(Paragraph(timestamp, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Process content
    sections = content.split('\n\n')
    
    for section in sections:
        if section.strip():
            # Check if it's a heading
            if section.startswith('# '):
                story.append(Paragraph(section[2:].strip(), heading_style))
            elif section.startswith('## '):
                story.append(Paragraph(section[3:].strip(), styles['Heading3']))
            # Regular paragraph
            else:
                # Handle special characters for PDF
                safe_content = section.replace('<', '&lt;').replace('>', '&gt;')
                # Handle bullet points
                if safe_content.strip().startswith(('- ', '* ')):
                    for line in safe_content.split('\n'):
                        if line.strip().startswith(('- ', '* ')):
                            story.append(Paragraph(f"• {line.strip()[2:]}", styles['Normal']))
                        elif line.strip():
                            story.append(Paragraph(line.strip(), styles['Normal']))
                else:
                    story.append(Paragraph(safe_content, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    print(f"✅ PDF file created: {filepath}")
    return filepath


def generate_document(content: str, format: str = "txt", title: str = "Generated Document", filename: str = None) -> str:
    """
    Main function to generate documents in different formats.
    
    Args:
        content: The text content to be included in the document
        format: 'txt', 'docx', or 'pdf'
        title: Document title (used for DOCX and PDF)
        filename: Custom filename (optional)
    
    Returns:
        filepath: Path to the generated file
    """
    format = format.lower().strip()
    
    if format == 'txt' or format == '.txt':
        return create_txt_file(content, filename)
    elif format == 'docx' or format == '.docx':
        return create_docx_file(content, title, filename)
    elif format == 'pdf' or format == '.pdf':
        return create_pdf_file(content, title, filename)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'txt', 'docx', or 'pdf'")