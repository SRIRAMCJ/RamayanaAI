"""
=====================================================
Ramayana AI
Production Retriever
=====================================================
"""

from pathlib import Path
import chromadb

from embeddings.embedding_model import load_embedding_model


class Retriever:

    def __init__(self):

        print("=" * 60)
        print("Initializing Retriever...")
        print("=" * 60)

        self.embedding_model = load_embedding_model()

        project_root = Path(__file__).resolve().parent.parent.parent
        chroma_db = project_root / "Database" / "chroma_db"

        client = chromadb.PersistentClient(path=str(chroma_db))

        self.collection = client.get_collection(
            name="ramayana_collection"
        )

        print("Retriever Ready!")
        print("=" * 60)

    # ---------------------------------------------------------

    def retrieve(self, question: str, top_k: int = 10):

        question = question.strip()

        print("\n" + "=" * 60)
        print(f"Searching: {question}")
        print("=" * 60)

        question_embedding = self.embedding_model.encode(
            question,
            normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results=max(top_k, 10)
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        passages = []

        for doc, meta, distance in zip(documents, metadatas, distances):

            if not doc:
                continue

            doc = doc.strip()

            if not doc:
                continue

            canto = meta.get("canto", "")

            if isinstance(canto, dict):
                canto = (
                    f"{canto.get('number', '')} - "
                    f"{canto.get('title', '')}"
                )

            passages.append(
                {
                    "text": doc,
                    "book": meta.get("book", ""),
                    "canto": canto,
                    "page": meta.get("page", ""),
                    "chunk": meta.get("chunk", ""),
                    "score": float(distance),
                }
            )

        # Lower distance = better match
        passages.sort(key=lambda x: x["score"])

        cleaned = []
        seen = set()

        for p in passages:

            if p["text"] in seen:
                continue

            seen.add(p["text"])

            cleaned.append(p)

            if len(cleaned) >= top_k:
                break

        print("\nRetrieved Passages")

        for i, p in enumerate(cleaned, start=1):
            print(
                f"{i}. Score={p['score']:.4f} | "
                f"{p['book']} | "
                f"{p['canto']} | "
                f"Page {p['page']}"
            )

        print(f"\nRetrieved {len(cleaned)} relevant passages.")

        return cleaned


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    retriever = Retriever()

    passages = retriever.retrieve(
        "Who is Hanuman?"
    )

    for i, p in enumerate(passages, start=1):

        print("\n" + "=" * 60)
        print(f"PASSAGE {i}")
        print("=" * 60)
        print("Book :", p["book"])
        print("Canto:", p["canto"])
        print("Page :", p["page"])
        print("Score:", round(p["score"], 4))
        print()
        print(p["text"][:500])