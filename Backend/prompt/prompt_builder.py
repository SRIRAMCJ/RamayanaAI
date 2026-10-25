"""
=========================================================
Ramayana AI
Prompt Builder
=========================================================
"""

from typing import List, Dict


class PromptBuilder:

    def __init__(self):
        pass

    # ------------------------------------------------------

    def build_prompt(
        self,
        question: str,
        retrieved_chunks: List[Dict]
    ) -> str:

        passages = []

        for chunk in retrieved_chunks:
            text = chunk["text"].strip()

            if text:
                passages.append(text)

        context = "\n\n".join(passages)

        prompt = f"""
Context:

{context}

Question:

{question}

Answer:
"""

        return prompt