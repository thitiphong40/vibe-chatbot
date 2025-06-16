from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os

def generate_alphabet_numbers_pdf():
    # Create documents directory if it doesn't exist
    if not os.path.exists('documents'):
        os.makedirs('documents')
    
    # Create PDF file
    pdf_path = os.path.join('documents', 'alphabet_numbers.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title = Paragraph("Alphabet and Numbers Reference", styles['Title'])
    story.append(title)
    story.append(Paragraph("<br/><br/>", styles['Normal']))
    
    # Add alphabet section
    story.append(Paragraph("Alphabet (A-Z):", styles['Heading1']))
    alphabet_text = " ".join([chr(i) for i in range(65, 91)])  # A-Z
    story.append(Paragraph(alphabet_text, styles['Normal']))
    story.append(Paragraph("<br/><br/>", styles['Normal']))
    
    # Add numbers section
    story.append(Paragraph("Numbers (1-99):", styles['Heading1']))
    numbers_text = " ".join([str(i) for i in range(1, 100)])
    story.append(Paragraph(numbers_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    generate_alphabet_numbers_pdf() 