"""
=========================================================
Ramayana AI
Prompt Builder (OPTIMIZED)
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
        """
        Build a structured prompt that encourages detailed answers.
        Provide clear context and signal that comprehensive answers are expected.
        """

        passages = []

        for chunk in retrieved_chunks:
            text = chunk["text"].strip()

            if text:
                passages.append(text)

        context = "\n\n".join(passages)

        # ===== OPTIMIZED PROMPT STRUCTURE =====
        prompt = f"""Context from the Valmiki Ramayana:

{context}

---

Question: {question}

---

Provide a comprehensive answer based on the context above. Include relevant details, characteristics, and relationships. Answer in complete sentences.

Answer:"""

        return prompt
