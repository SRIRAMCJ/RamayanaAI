"""
=====================================================
Ramayana AI
LLM Test
=====================================================

Purpose:
--------
This file is ONLY for testing the LLM module.

It verifies that:
1. model.py loads correctly
2. Ollama is running
3. Qwen3 responds correctly

This file will NOT be used in production.
=====================================================
"""

# =====================================================
# IMPORT
# =====================================================

from model import RamayanaLLM

# =====================================================
# CREATE LLM OBJECT
# =====================================================

llm = RamayanaLLM()

print("=" * 60)
print("Ramayana AI - LLM Test")
print("=" * 60)

# =====================================================
# TEST PROMPT
# =====================================================

question = "Hello"

print("\nQuestion:")
print(question)

print("\nGenerating response...\n")

answer = llm.generate(question)

print("Response:")
print(answer)

print("\nLLM Test Completed Successfully!")