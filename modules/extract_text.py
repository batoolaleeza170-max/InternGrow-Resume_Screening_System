import fitz  # PyMuPDF
from docx import Document

# PDF Text Extraction
def extract_pdf(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


# DOCX Text Extraction
def extract_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# Detect File Type
def extract_text(file):

    if file.name.endswith(".pdf"):
        return extract_pdf(file)

    elif file.name.endswith(".docx"):
        return extract_docx(file)

    else:
        return ""