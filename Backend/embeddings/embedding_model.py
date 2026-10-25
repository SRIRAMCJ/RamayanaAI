"""
embedding_model.py

Loads and returns the SentenceTransformer embedding model.

Author: Sriram
Project: Ramayana AI
"""

from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "BAAI/bge-m3"


# --------------------------------------------------
# Embedding Model Loader
# --------------------------------------------------

def load_embedding_model():
    """
    Loads the embedding model.

    Returns:
        SentenceTransformer: Loaded embedding model.
    """

    print("=" * 60)
    print("Loading Embedding Model...")
    print("=" * 60)

    model = SentenceTransformer(MODEL_NAME)

    print(f"Successfully Loaded: {MODEL_NAME}")
    print("=" * 60)

    return model


# --------------------------------------------------
# Standalone Test
# --------------------------------------------------

if __name__ == "__main__":

    embedding_model = load_embedding_model()

    print("\nEmbedding Model Test Successful!")