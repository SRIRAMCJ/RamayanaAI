"""
=====================================================
Ramayana AI
Production RAG Pipeline
=====================================================
"""

import time

from formatter.answer_formatter import AnswerFormatter
from retrieval.retriever import Retriever
from prompt.prompt_builder import PromptBuilder
from llm.model import RamayanaLLM


class RAGPipeline:

    def __init__(self):

        print("=" * 60)
        print("Initializing RAG Pipeline...")
        print("=" * 60)

        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.llm = RamayanaLLM()
        self.formatter = AnswerFormatter()

        print("RAG Pipeline Ready!")
        print("=" * 60)

    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
        language: str = "en",
        ):

        start_time = time.time()

        question = question.strip()

        if not question:
            return "Please ask a valid question."

        print("\n" + "=" * 80)
        print("QUESTION")
        print("=" * 80)
        print(question)

        # -----------------------------------------------------
        # RETRIEVE
        # -----------------------------------------------------

        retrieved_chunks = self.retriever.retrieve(
            question,
            top_k=10
            )
    

        if not retrieved_chunks:
            return (
                "I searched the uploaded Ramayana but could not find "
                "enough information to answer this question."
            )

        print(f"\nRetrieved Chunks: {len(retrieved_chunks)}")

        print("\nTop Retrieved Chunks")
        print("-" * 80)

        cleaned_chunks = []

        for i, chunk in enumerate(retrieved_chunks, start=1):

            print(f"\nChunk {i}")
            print(f"Book : {chunk['book']}")
            print(f"Canto: {chunk['canto']}")
            print(f"Page : {chunk['page']}")
            print(f"Score: {round(chunk['score'], 4)}")

            preview = chunk["text"][:300].replace("\n", " ")
            print(preview)

            cleaned_chunks.append(
                {
                    "text": chunk["text"][:1200],
                    "book": chunk["book"],
                    "canto": chunk["canto"],
                    "page": chunk["page"],
                    "chunk": chunk["chunk"],
                    "score": chunk["score"],
                }
            )

        # -----------------------------------------------------
        # BUILD PROMPT
        # -----------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            question=question,
            retrieved_chunks=cleaned_chunks,
        )

        print("\n" + "=" * 80)
        print("PROMPT LENGTH")
        print("=" * 80)
        print(len(prompt))

        # -----------------------------------------------------
        # GENERATE ANSWER
        # -----------------------------------------------------

        print("\nGenerating Answer...\n")

        answer = self.llm.generate(
            prompt=prompt,
            language=language,
            )

        if answer is None:
            return "I could not generate an answer."

        answer = self.formatter.format(answer)

        if not answer:
            return "I could not generate an answer."

        print("\n" + "=" * 80)
        print("FINAL ANSWER")
        print("=" * 80)
        print(answer)

        # Print debug info to console (not added to response)
        print("\n" + "=" * 60)
        print("Debug Info (Not in API Response)")
        print("=" * 60)
        
        # Sources
        sources = []
        seen = set()

        for chunk in cleaned_chunks:
            canto = chunk["canto"]
            
            # Format canto properly if it's a dict
            if isinstance(canto, dict):
                canto = f"{canto.get('number', '')} - {canto.get('title', '')}"

            source = (
                chunk["book"],
                canto,
                chunk["page"],
            )

            if source not in seen:
                seen.add(source)
                sources.append(
                    f"• {chunk['book']} | Canto {canto} | Page {chunk['page']}"
                )

        if sources:
            print("\nSources")
            print("-" * 60)
            print("\n".join(sources))

        # Response info
        elapsed = time.time() - start_time
        print(f"\nModel            : Qwen3-4B")
        print(f"Retrieved Chunks : {len(cleaned_chunks)}")
        print(f"Response Time    : {elapsed:.2f} seconds")
        print(f"Language         : English")

        # Return ONLY the answer
        return answer


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    rag = RAGPipeline()

    while True:

        print()

        question = input("Ask: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = rag.ask(question)

        print("\n" + "=" * 80)
        print(answer)
        print("=" * 80)