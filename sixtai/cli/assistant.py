# assistant.py

import openai
import os

def explain_failure(prompt: str, response: str, latency: float) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        return "⚠️ Missing OPENAI_API_KEY environment variable."

    system_prompt = """You are an LLM observability expert. Given a user prompt, an LLM response, and metadata like latency or failure patterns, explain what might have gone wrong. Provide clear, actionable advice. Be concise."""

    user_message = f"""
Prompt:
{prompt}

Response:
{response}

Latency: {latency:.2f}s

Is this output acceptable? If not, why? Suggest what might be improved.
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        return completion["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Error during analysis: {str(e)}"
