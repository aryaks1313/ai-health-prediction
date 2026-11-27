import json

from groq import Groq, GroqError

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    AI_MODE
)


class AIServiceError(Exception):
    pass


def generate_health_remarks(
    glucose: float,
    haemoglobin: float,
    cholesterol: float
) -> str:

    if AI_MODE == "mock":
        return (
            "DEMO MODE: AI prediction not performed."
        )

    if not GROQ_API_KEY:
        raise AIServiceError(
            "Groq API key is not configured."
        )

    blood_results = {
        "glucose": glucose,
        "haemoglobin": haemoglobin,
        "cholesterol": cholesterol
    }

    system_prompt = """
You are an AI-assisted health risk assessment
assistant for an educational application.

Analyze the provided blood test values.

Assumed units:
Glucose: mg/dL
Haemoglobin: g/dL
Total cholesterol: mg/dL

Rules:
1. Identify possible abnormal values and associated risks.
2. Do not provide a confirmed medical diagnosis.
3. Do not prescribe medication or treatment.
4. Glucose fasting status is unknown.
5. Haemoglobin reference ranges may depend on
   age, sex and clinical context.
6. Do not invent missing patient information.
7. Recommend appropriate professional medical review.
8. Do not provide numerical disease probabilities.
9. Return a short professional paragraph in English.
10. If values appear within common ranges, do not
    claim that the patient is disease-free.
"""

    try:

        client = Groq(
            api_key=GROQ_API_KEY,
            timeout=30.0,
            max_retries=1
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(blood_results)
                }
            ],
            temperature=0.2,
            max_completion_tokens=1024
        )

        remarks = response.choices[0].message.content

        if not remarks or not remarks.strip():
            raise AIServiceError(
                "No prediction returned by AI."
            )

        return remarks.strip()

    except GroqError as exc:

        raise AIServiceError(
            "AI service unavailable. Please retry."
        ) from exc