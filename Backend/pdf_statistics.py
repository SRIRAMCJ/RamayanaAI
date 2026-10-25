from pathlib import Path
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "Books"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

doc = pymupdf.open(PDF_FILE)

empty_pages = 0
text_pages = 0
total_characters = 0

largest_page = 0
largest_chars = 0

for i, page in enumerate(doc):

    text = page.get_text().strip()

    chars = len(text)

    total_characters += chars

    if chars == 0:
        empty_pages += 1
    else:
        text_pages += 1

    if chars > largest_chars:
        largest_chars = chars
        largest_page = i + 1

print("=" * 80)
print("RAMAYANA PDF STATISTICS")
print("=" * 80)

print(f"File               : {PDF_FILE.name}")
print(f"Total Pages        : {len(doc)}")
print(f"Pages with Text    : {text_pages}")
print(f"Empty Pages        : {empty_pages}")
print(f"Total Characters   : {total_characters:,}")
print(f"Largest Page       : {largest_page}")
print(f"Largest Characters : {largest_chars}")

doc.close()