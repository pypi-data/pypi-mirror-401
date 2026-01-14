import os
import requests
from typing import Optional

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SUPPORTED_MODELS = {
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
}

def generate_commit(
    diff: str,
    api_key: Optional[str],
    model: str,
) -> str:
    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("Groq API key not provided")

    if model not in SUPPORTED_MODELS:
        raise RuntimeError(
            f"Unsupported Groq model '{model}'. "
            f"Supported models: {', '.join(SUPPORTED_MODELS)}"
        )

    prompt = f"""
You are a senior software engineer.
Generate a concise conventional git commit message.

Rules:
- Max 72 characters
- Imperative tone
- No explanation
- Use feat/fix/refactor/docs/test/chore

Git diff:
{diff}
"""

    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You generate excellent, concise git commit messages.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 100,
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error {response.status_code}: {response.text}"
        )

    return response.json()["choices"][0]["message"]["content"].strip()
