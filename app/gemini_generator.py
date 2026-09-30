import os
from google import genai


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.1-pro-preview"


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day beginner-friendly fitness plan.

User information:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Give a clear 7-day plan.
- Include the day number and day name.
- Include exercises, sets/reps or duration, and rest periods where appropriate.
- Include at least one recovery/rest day.
- Keep the plan practical and easy to understand.
- Do not give dangerous or extreme exercise instructions.
- Do not recommend extreme dieting or unsafe weight-loss methods.
- Mention that the user should stop if they experience pain, dizziness, or unusual symptoms.
- Keep the answer suitable for a general fitness application.

Format the answer clearly with headings for Day 1 through Day 7.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text