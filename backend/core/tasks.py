from celery import shared_task
from .utils.plan_engine import generate_workout_plan
from .utils.meal_engine import generate_meal_plan
from content.utils.meme_engine import fetch_donkey_gif, generate_meme_caption

@shared_task
def generate_plan_task(goal: str, activity_types=None, tone: str = "supportive"):
    return generate_workout_plan(goal, activity_types, tone)

@shared_task
def generate_meal_plan_task(goal: str, tone: str = "supportive", mood: str | None = None):
    return generate_meal_plan(goal, tone, mood)

@shared_task
def generate_meme_task(tone: str = "funny"):
    return {
        "image_url": fetch_donkey_gif(),
        "caption": generate_meme_caption(tone),
    }
