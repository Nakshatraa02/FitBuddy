from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, User
from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    user_input = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    workout_plan = generate_workout_gemini(
        user_input.username,
        user_input.age,
        user_input.weight,
        user_input.goal,
        user_input.intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        user_input.goal,
        user_input.intensity
    )

    db: Session = SessionLocal()

    try:
        user = User(
            user_id=user_input.user_id,
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            original_workout_plan=workout_plan,
            updated_workout_plan=None,
            nutrition_tip=nutrition_tip,
            feedback=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "message": "Your personalized workout plan has been generated!"
            }
        )

    finally:
        db.close()


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    feedback_request = FeedbackRequest(
        user_id=user_id,
        feedback=feedback
    )

    db: Session = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == feedback_request.user_id)
            .order_by(User.id.desc())
            .first()
        )

        if not user:
            return HTMLResponse(
                content="User not found.",
                status_code=404
            )

        current_plan = (
            user.updated_workout_plan
            or user.original_workout_plan
        )

        updated_plan = update_workout_plan(
            user.username,
            user.age,
            user.weight,
            user.goal,
            user.intensity,
            current_plan,
            feedback_request.feedback
        )

        user.feedback = feedback_request.feedback
        user.updated_workout_plan = updated_plan

        db.commit()
        db.refresh(user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "message": "Your workout plan has been updated using your feedback!"
            }
        )

    finally:
        db.close()