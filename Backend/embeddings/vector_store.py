from pathlib import Path
import json

import chromadb

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"
DATABASE_DIR = PROJECT_ROOT / "Database"

INPUT_FILE = KNOWLEDGE_DIR / "knowledge_embeddings.json"

CHROMA_DB_DIR = DATABASE_DIR / "chroma_db"

# =====================================================
# CREATE DATABASE DIRECTORY
# =====================================================

CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Database Folder Ready")
print(CHROMA_DB_DIR)
print("=" * 60)

# =====================================================
# CONNECT TO CHROMADB
# =====================================================

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)

print("Connected Successfully!")

# Create the collection once; upsert below makes this script safe to rerun.
collection = client.get_or_create_collection(name="ramayana_collection")

print("Collection Created!")

# =====================================================
# LOAD KNOWLEDGE EMBEDDINGS
# =====================================================

print("\nLoading knowledge embeddings...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks.")

# =====================================================
# INSERT INTO CHROMADB
# =====================================================

print("\nAdding embeddings to ChromaDB...")

batch_size = 500
for offset in range(0, len(chunks), batch_size):
    batch = chunks[offset:offset + batch_size]
    collection.upsert(
        ids=[str(chunk["id"]) for chunk in batch],
        embeddings=[chunk["embedding"] for chunk in batch],
        documents=[chunk["text"] for chunk in batch],
        metadatas=[
            {
                "book": chunk.get("book", ""),
                "canto": str(chunk.get("canto", "")),
                "page": chunk.get("page", 0),
                "chunk": chunk.get("chunk", 0),
            }
            for chunk in batch
        ],
    )
    print(f"Indexed {min(offset + batch_size, len(chunks))}/{len(chunks)} chunks...")

print("\nAll embeddings added successfully!")
print(f"Total Chunks Stored: {collection.count()}")
