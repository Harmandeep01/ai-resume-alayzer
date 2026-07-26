from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for pages in reader.pages:
        current_text = pages.extract_text()
        if current_text:
            text += current_text
    return text