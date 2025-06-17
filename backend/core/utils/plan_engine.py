from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import os

from . import clean_text

load_dotenv()
client = OpenAI()


def generate_workout_plan(goal: str, activity_types: List[str] | None = None, tone: str = "supportive") -> Dict[str, List[str]]:
    """Generate a simple 7-day workout plan using OpenAI."""
    goal_text = goal or "general fitness"
    activities = ", ".join(activity_types) if activity_types else "any activities"

    tone_map = {
        "supportive": "Write with encouragement and positivity.",
        "savage": "Use a tough-love style with playful insults.",
        "donkey": "Inject donkey-themed humor throughout.",
    }
    tone_instructions = tone_map.get(tone, "Use a friendly tone.")

    prompt = (
        f"Create a short 7-day workout plan to help with {goal_text}. "
        f"Suggested activities include: {activities}. "
        f"{tone_instructions} "
        "Give each day on one line."
    )

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": "You're a fitness coach creating concise daily workout plans.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    text = clean_text(response.choices[0].message.content.strip())
    lines = [clean_text(line.strip()) for line in text.splitlines() if line.strip()]
    return {"plan": lines[:7]}
