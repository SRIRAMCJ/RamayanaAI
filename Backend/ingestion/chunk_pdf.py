from pathlib import Path
import json
import re

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"

INPUT_FILE = KNOWLEDGE_DIR / "structured_pages.json"
OUTPUT_FILE = KNOWLEDGE_DIR / "knowledge_chunks.json"

print("=" * 60)
print("Ramayana AI - Chunk Generator")
print("=" * 60)

# =====================================================
# LOAD STRUCTURED PAGES
# =====================================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    structured_pages = json.load(f)

print(f"Loaded {len(structured_pages)} structured pages.")

# =====================================================
# SETTINGS
# =====================================================

MAX_CHARS = 1200

knowledge_chunks = []

chunk_id = 1

empty_pages = 0
empty_chunks_skipped = 0

# =====================================================
# CREATE CHUNKS
# =====================================================

for page in structured_pages:

    page_text = page.get("text", "")

    # Skip completely empty pages
    if not page_text or not page_text.strip():
        empty_pages += 1
        continue

    paragraphs = re.split(r"\n\s*\n", page_text)

    current_text = ""
    current_chunk = 1

    for para in paragraphs:

        para = para.strip()

        # Skip blank paragraphs
        if not para:
            continue

        # Paragraph fits inside current chunk
        if len(current_text) + len(para) <= MAX_CHARS:

            current_text += para + "\n\n"

        else:

            # Save previous chunk ONLY if it contains text
            if current_text.strip():

                knowledge_chunks.append(
                    {
                        "id": f"CHUNK_{chunk_id:06d}",
                        "book": page["book"],
                        "canto": page["canto"],
                        "page": page["page"],
                        "chunk": current_chunk,
                        "text": current_text.strip(),
                    }
                )

                chunk_id += 1
                current_chunk += 1

            else:
                empty_chunks_skipped += 1

            # Start new chunk with current paragraph
            current_text = para + "\n\n"

    # Save remaining chunk
    if current_text.strip():

        knowledge_chunks.append(
            {
                "id": f"CHUNK_{chunk_id:06d}",
                "book": page["book"],
                "canto": page["canto"],
                "page": page["page"],
                "chunk": current_chunk,
                "text": current_text.strip(),
            }
        )

        chunk_id += 1

# =====================================================
# SAVE
# =====================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        knowledge_chunks,
        f,
        indent=4,
        ensure_ascii=False,
    )

# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)
print("Chunk Generation Completed")
print("=" * 60)
print(f"Total Chunks Created      : {len(knowledge_chunks)}")
print(f"Empty Pages Skipped       : {empty_pages}")
print(f"Empty Chunks Prevented    : {empty_chunks_skipped}")
print(f"Saved File               : {OUTPUT_FILE}")
print("=" * 60)