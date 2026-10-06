import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not configured")

client = Groq(api_key=api_key)


MODEL_NAME = "openai/gpt-oss-120b"

def ask_llm(prompt: str) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are InsightFlow AI, an intelligent "
                    "data analytics assistant. "
                    "Answer clearly and accurately."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content