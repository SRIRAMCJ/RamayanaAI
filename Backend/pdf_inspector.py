from pathlib import Path
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "Books"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

doc = pymupdf.open(PDF_FILE)

print("=" * 80)
print("RAMAYANA PDF INSPECTOR")
print("=" * 80)

print(f"File        : {PDF_FILE.name}")
print(f"Total Pages : {len(doc)}")

print("\nMetadata")
print("-" * 80)

for key, value in doc.metadata.items():
    print(f"{key:15}: {value}")

print("=" * 80)

for i in range(min(10, len(doc))):

    page = doc.load_page(i)

    text = page.get_text()

    print("\n")
    print("=" * 80)
    print(f"PAGE {i+1}")
    print("=" * 80)

    print(f"Characters : {len(text)}")

    if text.strip():
        print("\nPreview:\n")
        print(text[:3000])
    else:
        print("No text found.")

doc.close()