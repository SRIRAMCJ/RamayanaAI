"""
=====================================================
Ramayana AI
Answer Formatter
=====================================================
"""

import re
import textwrap


class AnswerFormatter:

    def __init__(self):
        pass

    def format(self, answer: str) -> str:

        if not answer:
            return ""

        # Remove excessive blank lines
        answer = re.sub(r"\n{3,}", "\n\n", answer.strip())

        paragraphs = []

        for paragraph in answer.split("\n"):

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            paragraphs.append(
                textwrap.fill(
                    paragraph,
                    width=100,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )

        return "\n\n".join(paragraphs)