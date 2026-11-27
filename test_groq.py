from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing")

client = Groq(api_key=GROQ_API_KEY)

response = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=[
        {
            "role": "user",
            "content": "Explain what haemoglobin is in one sentence."
        }
    ],
    max_completion_tokens=100
)

print(response.choices[0].message.content)