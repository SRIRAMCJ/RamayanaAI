"""
=====================================================
Ramayana AI
LLM Wrapper (OPTIMIZED)
=====================================================
"""

import json
import re

from ollama import chat


class RamayanaLLM:

    def __init__(self):
        self.model = "qwen3:4b"

        print("=" * 60)
        print(f"Using Ollama Model: {self.model}")
        print("=" * 60)

    # ---------------------------------------------------------

    def _clean_answer(self, answer: str) -> str:
        """
        OPTIMIZED: Remove ONLY thinking/reasoning markers.
        Preserve all substantive content about the actual answer.
        """
        if not answer:
            return ""

        # ===== STEP 1: Remove thinking/reasoning markers =====
        
        # Handle Qwen thinking tags
        if "_ITER_THINK_" in answer:
            answer = re.sub(
                r"_ITER_THINK_.*?_ITER_END_",
                "",
                answer,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        # Remove emoji-based thinking blocks (💭, 🤔, etc.)
        answer = re.sub(r"💭.*?🗣️", "", answer, flags=re.DOTALL | re.IGNORECASE).strip()
        answer = re.sub(r"🤔.*?🪧", "", answer, flags=re.DOTALL | re.IGNORECASE).strip()

        # Remove "Mouth" and "Think" tags if present
        if " Mouth" in answer:
            answer = answer.split(" Mouth", 1)[1].strip()
        
        if " Think" in answer:
            answer = re.sub(
                r" Think.*? Mouth", "", answer, flags=re.DOTALL | re.IGNORECASE
            ).strip()

        # Extract content after closing tags
        if "🗣️" in answer:
            answer = answer.split("🗣️", 1)[1].strip()
        
        if "🪧" in answer:
            answer = answer.split("🪧", 1)[1].strip()

        # ===== STEP 2: Remove ONLY metalanguage preambles =====
        # These start the answer but aren't part of the actual content
        
        metalanguage_patterns = [
            r"^I need to answer.*?(?=\n\n|\nBased on|\nAccording to|\nRamayana|\nThe|\nHe|\nShe|\nIt|\nThis)",
            r"^I'll answer.*?(?=\n\n|\nBased on|\nAccording to|\nRamayana|\nThe|\nHe|\nShe|\nIt|\nThis)",
            r"^Let me answer.*?(?=\n\n|\nBased on|\nAccording to|\nRamayana|\nThe|\nHe|\nShe|\nIt|\nThis)",
            r"^To answer.*?(?=\n\n|\nBased on|\nAccording to|\nRamayana|\nThe|\nHe|\nShe|\nIt|\nThis)",
        ]
        
        for pattern in metalanguage_patterns:
            match = re.search(pattern, answer, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if match:
                answer = answer[match.end():].strip()
                break  # Only apply once

        # ===== STEP 3: Clean up formatting =====
        
        # Remove leading/trailing bullets or numbers
        answer = re.sub(r'^\s*[-•*]\s+', '', answer, flags=re.MULTILINE)
        answer = re.sub(r'^\s*\d+\.\s+', '', answer, flags=re.MULTILINE)

        # Clean up multiple blank lines (keep structure)
        answer = re.sub(r'\n\n\n+', '\n\n', answer)

        # ===== STEP 4: Normalize for JSON output =====
        # Replace newlines with spaces for clean JSON response
        answer = re.sub(r'\n+', ' ', answer)

        # Clean up multiple spaces
        answer = re.sub(r'\s+', ' ', answer).strip()

        return answer

    # ---------------------------------------------------------

    def generate(
        self,
        prompt: str,
        language: str = "en",
    ) -> str:
        try:
            if language == "hi":
                language_instruction = """
Respond ONLY in Hindi.

Never use English.

Never use Chinese.

Never reveal your thinking.

Never reveal internal reasoning.

Write naturally in Hindi.
"""
            else:
                language_instruction = """
Respond ONLY in English.

Never use Hindi.

Never use Chinese.

Never reveal your thinking.

Never reveal internal reasoning.

Write naturally in English.
"""

            response = chat(
                model=self.model,
                think=False,
                options={
                    "temperature": 0.3,  # Increased from 0.1 for more varied output
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1,
                    "num_predict": 1500,  # Increased for more comprehensive answers
                    "num_ctx": 4096,
                },
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are Ramayana AI. Your role is to provide comprehensive, well-defined answers about the Ramayana.

{language_instruction}

INSTRUCTIONS:

1. Answer ONLY using the provided context.
2. Provide a COMPLETE, well-structured answer with:
   - Who/What is the subject
   - Key characteristics or roles
   - Relationships with other characters
   - Important events or significance
3. Give substantive information, not just one sentence.
4. Use natural language and proper sentence structure.
5. Never mention the context, passages, page numbers, book names, or canto numbers.
6. Never mention retrieval or sources.
7. Never output your thinking or reasoning process.
8. If the answer does not exist in the context, say: "I could not find this information in the indexed Valmiki Ramayana."

START WITH THE ANSWER DIRECTLY.
""",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            print("\n" + "=" * 80)
            print("RAW OLLAMA RESPONSE")
            print("=" * 80)
            print(json.dumps(response, indent=2, ensure_ascii=False, default=str))

            if response is None:
                return "I could not generate an answer."

            message = response.get("message", {})
            answer = message.get("content", "").strip()
            
            # Clean the answer (minimal cleaning only)
            answer = self._clean_answer(answer)

            if not answer:
                thinking = message.get("thinking", "").strip()
                if thinking:
                    print("\nWARNING: Model returned thinking only.")

                return "I could not generate a final answer."

            print("\n" + "=" * 80)
            print("FINAL ANSWER (After Cleaning)")
            print("=" * 80)
            print(answer)

            return answer

        except Exception as e:
            print("\n" + "=" * 80)
            print("OLLAMA ERROR")
            print("=" * 80)
            print(e)

            return f"Error: {e}"
