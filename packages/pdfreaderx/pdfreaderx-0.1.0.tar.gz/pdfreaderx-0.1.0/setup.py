from setuptools import setup, find_packages

setup(
    name="pdfreaderx",
    version="0.1.0",
    packages=["pdfreaderx"],
    install_requires=[
        "pdfplumber",
        "pytesseract",
        "pillow",
        "camelot-py[cv]",
        "PyMuPDF"
    ],
)
