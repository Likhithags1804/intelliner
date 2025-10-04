from io import StringIO
from PyPDF2 import PdfReader
import docx

def read_txt(file):
    return StringIO(file.getvalue().decode("utf-8")).read()

def read_pdf(file):
    reader = PdfReader(file)
    return "".join((p.extract_text() or "") for p in reader.pages)

def read_docx(file):
    d = docx.Document(file)
    return "\n".join(p.text for p in d.paragraphs)

def read_any(uploaded_file):
    if not uploaded_file:
        return ""
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "txt":  return read_txt(uploaded_file)
    if ext == "pdf":  return read_pdf(uploaded_file)
    if ext == "docx": return read_docx(uploaded_file)
    raise ValueError("Unsupported file type (use .txt, .pdf, .docx)")
