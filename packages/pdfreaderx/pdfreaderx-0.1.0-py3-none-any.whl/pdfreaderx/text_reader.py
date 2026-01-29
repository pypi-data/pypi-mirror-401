# pdfreader/text_reader.py
def extract_text(page):
    try:
        return page.extract_text(layout=True) or ""
    except Exception:
        return ""
