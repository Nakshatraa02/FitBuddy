import os
from google import genai


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def generate_nutrition_tip_with_flash(
    goal: str,
    intensity: str
) -> str:

    prompt = f"""
You are the nutrition and recovery assistant for FitBuddy.

User fitness goal: {goal}
Workout intensity: {intensity}

Give concise general nutrition and recovery guidance that supports
the user's fitness goal.

Include:
- Hydration
- Balanced meals
- Protein and carbohydrate sources
- Fruits and vegetables
- Sleep and recovery

Do not recommend crash diets, extreme calorie restriction,
supplements, or unsafe weight-loss methods.

Keep the answer practical and easy to understand.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text