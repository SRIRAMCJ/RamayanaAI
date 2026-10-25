from pathlib import Path
import json
import re

# ============================================
# PATHS
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"

RAW_FILE = KNOWLEDGE_DIR / "raw_pages.json"

OUTPUT_FILE = KNOWLEDGE_DIR / "structured_pages.json"

# ============================================
# LOAD RAW PAGES
# ============================================

with open(RAW_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)

current_book = None
current_canto = None

structured = []

# ============================================
# PROCESS
# ============================================

for page in pages:

    text = page["text"]

    # Detect Book
    book_match = re.search(r"BOOK\s+([IVXLC]+)", text, re.IGNORECASE)

    if book_match:
        current_book = "BOOK " + book_match.group(1)

    # Detect Canto
    canto_match = re.search(
        r"Canto\s+([IVXLC]+)\.\s*(.*)",
        text,
        re.IGNORECASE
    )

    if canto_match:
        current_canto = {
            "number": canto_match.group(1),
            "title": canto_match.group(2).strip()
        }

    structured.append({

        "page": page["page"],

        "book": current_book,

        "canto": current_canto,

        "text": text

    })

# ============================================
# SAVE
# ============================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        structured,
        f,
        indent=4,
        ensure_ascii=False
    )

print("=" * 60)
print("Structured pages:", len(structured))
print("Saved:", OUTPUT_FILE)
print("=" * 60)