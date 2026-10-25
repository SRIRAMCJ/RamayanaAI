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

# =====================================================
# DELETE OLD COLLECTION (if exists)
# =====================================================

print("\nChecking for existing collection...")

try:
    client.delete_collection("ramayana_collection")
    print("Old collection deleted.")
except Exception:
    print("No old collection found.")

# =====================================================
# CREATE NEW COLLECTION
# =====================================================

print("\nCreating new collection...")

collection = client.create_collection(
    name="ramayana_collection"
)

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

for i, chunk in enumerate(chunks, start=1):

    collection.add(
        ids=[chunk["id"]],
        embeddings=[chunk["embedding"]],
        documents=[chunk["text"]],
        metadatas=[
            {
                "book": chunk["book"],
                "canto": str(chunk["canto"]),
                "page": chunk["page"],
                "chunk": chunk["chunk"]
            }
        ]
    )

    if i % 500 == 0:
        print(f"Inserted {i}/{len(chunks)} chunks...")

print("\nAll embeddings added successfully!")
print(f"Total Chunks Stored: {collection.count()}")