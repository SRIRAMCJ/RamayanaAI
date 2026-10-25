from pathlib import Path
import pymupdf

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "Books"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

# -------------------------------------------------
# Open PDF
# -------------------------------------------------

doc = pymupdf.open(PDF_FILE)

print("=" * 80)
print("RAMAYANA AI - READ PDF")
print("=" * 80)

print(f"File : {PDF_FILE.name}")
print(f"Pages: {len(doc)}")

print("\nFirst Page:\n")
print("-" * 80)

page = doc.load_page(0)

print(page.get_text())

doc.close()