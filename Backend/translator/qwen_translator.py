import ollama


class QwenTranslator:

    def __init__(self):

        self.model = "qwen3:4b"


    def hindi_to_english(self, text: str):

        prompt = f"""
Translate the following Hindi text into English.

Rules:

- Translate exactly.
- Do not summarize.
- Do not explain.
- Preserve names exactly.
- Return ONLY the English translation.

Hindi:

{text}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"].strip()


    def english_to_hindi(self, text: str):

        prompt = f"""
Translate the following English text into Hindi.

STRICT RULES:

- Translate only.
- Never summarize.
- Never rewrite.
- Never answer the question.
- Never explain.
- Preserve all names exactly.
- Preserve meaning exactly.
- Keep every sentence.
- Return ONLY the Hindi translation.

English:

{text}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"].strip()