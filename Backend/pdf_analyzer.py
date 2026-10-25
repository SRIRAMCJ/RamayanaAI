from pathlib import Path
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "Books"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

doc = pymupdf.open(PDF_FILE)

print("=" * 80)
print("RAMAYANA AI - PDF ANALYZER")
print("=" * 80)

print("File :", PDF_FILE.name)
print("Pages:", len(doc))

print("\nMetadata")
print(doc.metadata)

for i in range(min(10, len(doc))):

    page = doc.load_page(i)

    print("\n" + "=" * 80)
    print(f"PAGE {i+1}")
    print("=" * 80)

    print("\n----- TEXT -----\n")
    print(page.get_text()[:2500])

    print("\n----- BLOCKS -----\n")
    print(page.get_text("blocks")[:5])

    print("\n----- WORDS -----\n")
    print(page.get_text("words")[:20])

doc.close()