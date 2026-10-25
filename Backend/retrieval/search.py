from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATABASE_DIR = PROJECT_ROOT / "Database"
CHROMA_DB_DIR = DATABASE_DIR / "chroma_db"
# =====================================================
# CONNECT TO CHROMADB
# =====================================================

print("=" * 60)
print("Connecting to ChromaDB...")
print("=" * 60)

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)

print("Connected Successfully!")
# =====================================================
# LOAD COLLECTION
# =====================================================

print("\nLoading Ramayana Collection...")

collection = client.get_collection(
    name="ramayana_collection"
)

print("Collection Loaded Successfully!")
print(f"Total Documents: {collection.count()}")

# =====================================================
# CHECK FIRST DOCUMENT STORED IN CHROMADB
# =====================================================

print("\nChecking CHUNK_000001...\n")

sample = collection.get(
    ids=["CHUNK_000001"],
    include=["documents", "metadatas"]
)

print(sample)

# =====================================================
# VERIFY STORED DATA
# =====================================================

print("\nChecking first stored document...\n")

sample = collection.get(
    ids=["CHUNK_000001"],
    include=["documents", "metadatas"]
)

print(sample)

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

print("\nLoading Embedding Model...")

model = SentenceTransformer("BAAI/bge-m3")

print("Embedding Model Loaded!")

# =====================================================
# USER QUESTION
# =====================================================

question = "Who is Hanuman?"

print("\nQuestion:")
print(question)
# =====================================================
# GENERATE QUESTION EMBEDDING
# =====================================================

print("\nGenerating Question Embedding...")

question_embedding = model.encode(
    question,
    normalize_embeddings=True
)

print("Question Embedding Generated!")
print(f"Embedding Dimension: {len(question_embedding)}")
# =====================================================
# SEARCH CHROMADB
# =====================================================

print("\nSearching ChromaDB...")

results = collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=5
)

print("Search Completed!")
print("\nRaw Search Result:")

print(results)