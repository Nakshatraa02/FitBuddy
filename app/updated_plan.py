import os
from google import genai


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.1-pro-preview"


def update_workout_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    current_plan: str,
    feedback: str
) -> str:

    prompt = f"""
You are FitBuddy's workout-plan update assistant.

User:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Current workout plan:
{current_plan}

User feedback:
{feedback}

Create an updated 7-day workout plan based on the feedback.

Requirements:
- Keep the same general fitness goal.
- Adjust exercises, duration, sets/reps, or rest when appropriate.
- Clearly show Day 1 through Day 7.
- Include recovery/rest.
- Keep the plan practical and safe.
- Do not recommend extreme or dangerous exercise.
- Do not recommend extreme dieting.
- If the feedback suggests pain or injury, prioritize stopping the problematic
  activity and recommend seeking appropriate professional advice.

Return only the updated workout plan.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text