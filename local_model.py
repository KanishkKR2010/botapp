"""
Optional local-model integration point.

Keep this file offline. A future version can connect this function to
a local LLM runtime such as llama.cpp or another locally installed engine.

The function should return a plain string:
    answer = generate("Explain Python dictionaries")
"""
def generate(prompt: str) -> str:
    raise NotImplementedError(
        "No generative local model is installed. "
        "Use the built-in tutor or add a local LLM runtime."
    )
