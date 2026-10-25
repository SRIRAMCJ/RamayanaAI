"""
=====================================================
Ramayana AI
LLM Wrapper
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
        if not answer:
            return ""

        # Handle Qwen thinking tags properly
        if "_ITER_THINK_" in answer:
            answer = re.sub(
                r"_ITER_THINK_.*?_ITER_END_",
                "",
                answer,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        if " Mouth" in answer:
            answer = answer.split(" Mouth", 1)[1].strip()

        if " Think" in answer:
            answer = re.sub(
                r" Think.*? Mouth",
                "",
                answer,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        # Remove everything up to the closing  🗣️ tag
        if "🗣️" in answer:
            answer = answer.split("🗣️", 1)[1].strip()

        # Remove any remaining 💭 blocks
        answer = re.sub(
            r"💭.*?🗣️",
            "",
            answer,
            flags=re.DOTALL | re.IGNORECASE,
        ).strip()

        # Remove everything up to the closing  🪧 tag
        if "🪧" in answer:
            answer = answer.split("🪧", 1)[1].strip()

        # Remove any remaining  🤔 blocks
        answer = re.sub(
            r"🤔.*?🪧",
            "",
            answer,
            flags=re.DOTALL | re.IGNORECASE,
        ).strip()

        # AGGRESSIVE: Find where actual answer likely starts
        # Remove everything before the first substantive sentence about the topic
        
        # Patterns that indicate reasoning/analysis start
        reasoning_start_patterns = [
            r"^i need to answer.*?(?=\n\n[A-Z]|\n[A-Z])",
            r"^i'll .*?(?=\n\n[A-Z]|\n[A-Z])",
            r"^let me .*?(?=\n\n[A-Z]|\n[A-Z])",
            r"^to answer.*?(?=\n\n[A-Z]|\n[A-Z])",
        ]
        
        for pattern in reasoning_start_patterns:
            match = re.search(pattern, answer, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if match:
                # Remove from start up to where actual answer begins
                answer = answer[match.end():].strip()

        # Remove line-by-line reasoning
        lines = answer.split('\n')
        cleaned_lines = []
        
        for line in lines:
            text = line.strip()
            
            # Skip empty lines initially, but preserve structure
            if not text:
                cleaned_lines.append("")
                continue
            
            # Skip reasoning patterns
            skip_patterns = [
                r"^i need to",
                r"^i'll ",
                r"^i will ",
                r"^let me",
                r"^let's",
                r"^to answer",
                r"^based on the",
                r"^from the",
                r"^according to",
                r"^this passage",
                r"^the passage",
                r"^from passage",
                r"^in the passage",
                r"^the answer",
                r"^here",
                r"^so ",
                r"^the passages",
                r"^\d+\.",
                r"^bullet",
                r"^analysis:",
                r"^reasoning:",
                r"^thinking:",
                r"^summary:",
                r"^conclusion:",
                r"^based on information",
                r"^the question",
                r"^the topic",
                r"^first,",
                r"^secondly,",
                r"^finally,",
                r"^in summary",
                r"^after reviewing",
                r"^looking at",
                r"^examining",
                r"^reviewing",
                r"^from all these",
                r"^the answer should",
                r"^it should be",
                r"^we can see",
                r"^we know",
                r"^obviously",
                r"^clearly",
                r"^as we can see",
                r"^based on what",
                r"^the information",
                r"^this shows",
                r"^this indicates",
                r"^this demonstrates",
                r"^the key point",
                r"^importantly",
                r"^notably",
                r"^interesting",
            ]
            
            skip = False
            for pattern in skip_patterns:
                if re.match(pattern, text, re.IGNORECASE):
                    skip = True
                    break
            
            if not skip:
                cleaned_lines.append(text)
        
        answer = '\n'.join(cleaned_lines).strip()

        # Clean up multiple blank lines
        answer = re.sub(r'\n\n\n+', '\n\n', answer)

        # Remove leading dashes or bullets
        answer = re.sub(r'^\s*[-•*]\s+', '', answer, flags=re.MULTILINE)

        # Remove stray numbering
        answer = re.sub(r'^\s*\d+\.\s+', '', answer, flags=re.MULTILINE)

        # Final cleanup - remove any remaining analysis-like content at the beginning
        lines = answer.split('\n\n')
        if lines and len(lines[0]) < 100 and any(keyword in lines[0].lower() for keyword in ['answer', 'should be', 'will be', 'must be', 'need', 'craft', 'write']):
            lines = lines[1:]
        
        answer = '\n\n'.join(lines).strip()

        # ===== NEW: HANDLE NEWLINES FOR JSON =====
        # Replace all newlines with spaces to create clean JSON
        answer = re.sub(r'\n+', ' ', answer)  # Replace all newlines with space

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
                    "temperature": 0.1,  # Lower temperature for more deterministic output
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1,
                    "num_predict": 1000,  # Increased to get complete answers
                    "num_ctx": 4096,
                },
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are Ramayana AI.

{language_instruction}

You are Ramayana AI.

Answer ONLY using the provided context.

Rules:

- Give only the final answer.
- Never explain your reasoning.
- Never repeat the question.
- Never mention the context.
- Never mention passages.
- Never mention page numbers.
- Never mention book names.
- Never mention canto numbers.
- Never mention retrieval.
- Never output your thinking.

Start immediately with the answer.

If the answer does not exist in the context say

"I could not find this information in the indexed Valmiki Ramayana."

Output ONLY the final answer.
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
            
            # Removed the duplicated cleanup call you had here
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