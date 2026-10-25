from prompt_builder import PromptBuilder

builder = PromptBuilder()

question = "Who is Hanuman?"

context = """
Hanuman is the son of Vayu.

He is one of the greatest devotees of Lord Rama.

He crossed the ocean to Lanka in search of Sita.
"""

prompt = builder.build_prompt(
    question=question,
    context=context
)

print(prompt)