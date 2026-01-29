# pdfreader/image_reader.py
import fitz
import pytesseract
from PIL import Image
import io

def extract_images_ocr(pdf_path, page_number):
    text = ""
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]

    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]

        image = Image.open(io.BytesIO(image_bytes))
        text += pytesseract.image_to_string(image)

    return text.strip()
