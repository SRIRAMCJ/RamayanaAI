from pathlib import Path
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = PROJECT_ROOT / "Books"

PDF_FILE = BOOKS_DIR / "RAMAYANA_ENG.pdf"

doc = pymupdf.open(PDF_FILE)

print("=" * 80)
print("RAMAYANA PAGE EXPLORER")
print("=" * 80)

print(f"Loaded : {PDF_FILE.name}")
print(f"Pages  : {len(doc)}")

while True:

    value = input("\nEnter page number (q to quit): ")

    if value.lower() == "q":
        break

    try:

        page_no = int(value)

        if page_no < 1 or page_no > len(doc):
            print("Invalid page.")
            continue

        page = doc.load_page(page_no - 1)

        text = page.get_text()

        print("\n" + "=" * 80)
        print(f"PAGE {page_no}")
        print("=" * 80)

        print(text[:6000])

    except Exception as e:
        print("Error:", e)

doc.close()