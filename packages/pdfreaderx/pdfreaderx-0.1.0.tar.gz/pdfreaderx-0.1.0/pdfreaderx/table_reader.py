# pdfreader/table_reader.py
import camelot

def extract_tables(pdf_path, page_number):
    try:
        tables = camelot.read_pdf(pdf_path, pages=str(page_number))
        return [table.df.to_dict() for table in tables]
    except Exception:
        return []
