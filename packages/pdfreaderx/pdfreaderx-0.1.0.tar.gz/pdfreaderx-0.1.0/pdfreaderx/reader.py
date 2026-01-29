# pdfreader/reader.py
import pdfplumber
from .text_reader import extract_text
from .image_reader import extract_images_ocr
from .table_reader import extract_tables

def read_pdf(pdf_path):
    result = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_data = {
                "page_number": i + 1,
                "text": extract_text(page),
                "tables": extract_tables(pdf_path, i + 1),
                "images_text": extract_images_ocr(pdf_path, i + 1)
            }
            result.append(page_data)

    return result
