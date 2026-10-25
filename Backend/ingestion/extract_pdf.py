from pathlib import Path
import json
import pymupdf

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

BOOKS_DIR = PROJECT_ROOT / "Books"
KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

OUTPUT_FILE = KNOWLEDGE_DIR / "raw_pages.json"

KNOWLEDGE_DIR.mkdir(exist_ok=True)

# =====================================================
# OPEN PDF
# =====================================================

print("=" * 70)
print("RAMAYANA AI - PDF EXTRACTION")
print("=" * 70)

doc = pymupdf.open(PDF_FILE)

print(f"PDF : {PDF_FILE.name}")
print(f"Pages : {len(doc)}")

# =====================================================
# EXTRACT
# =====================================================

pages = []

for page_number, page in enumerate(doc, start=1):

    text = page.get_text()

    text = text.replace("\x00", "")

    text = text.strip()

    pages.append({

        "page": page_number,

        "text": text

    })

print(f"\nExtracted Pages : {len(pages)}")

# =====================================================
# SAVE
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        pages,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nSaved : {OUTPUT_FILE}")

doc.close()

print("\nDone.")