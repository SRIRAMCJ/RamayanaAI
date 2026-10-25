from pathlib import Path
import json

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"
DATABASE_DIR = PROJECT_ROOT / "Database"

INPUT_FILE = KNOWLEDGE_DIR / "knowledge_embeddings.json"

CHROMA_DB_DIR = DATABASE_DIR / "chroma_db"
# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"
DATABASE_DIR = PROJECT_ROOT / "Database"

INPUT_FILE = KNOWLEDGE_DIR / "knowledge_chunks.json"
OUTPUT_FILE = KNOWLEDGE_DIR / "knowledge_embeddings.json"

# =====================================================
# LOAD MODEL
# =====================================================

print("=" * 60)
print("Loading embedding model...")
print("=" * 60)

model = SentenceTransformer("BAAI/bge-m3")

print("Model Loaded Successfully!")

# =====================================================
# LOAD CHUNKS
# =====================================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# =====================================================
# GENERATE EMBEDDINGS
# =====================================================

print("\nGenerating embeddings...")

for chunk in tqdm(chunks):

    embedding = model.encode(
        chunk["text"],
        normalize_embeddings=True
    )

    chunk["embedding"] = embedding.tolist()

print("Embeddings Generated!")
# =====================================================
# SAVE EMBEDDINGS
# =====================================================

print("\nSaving embeddings...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=4
    )

print(f"Saved embeddings to:\n{OUTPUT_FILE}")