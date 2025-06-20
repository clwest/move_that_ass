from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict

from core.utils import clean_text

load_dotenv()
try:
    client = OpenAI()
except Exception:
    client = None


def generate_challenge(
    mood: str,
    missed_workouts: int,
    shame_streak: int,
    herd_size: int,
    tone: str = "mixed",
) -> Dict[str, str | int]:
    """Generate a short fitness challenge based on user history."""
    prompt = (
        "This user has {shame_streak} shame posts recently and {missed_workouts} missed workouts. "
        "They are in a herd of {herd_size} members and feel '{mood}'. "
        "Write a {tone} 3-7 day challenge in one to two sentences. "
        "Respond in JSON with keys 'challenge_text' and 'days'."
    ).format(
        shame_streak=shame_streak,
        missed_workouts=missed_workouts,
        herd_size=herd_size,
        mood=mood,
        tone=tone,
    )

    if client is None:
        text = "Do 20 jumping jacks each day"
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a motivational donkey crafting short "
                            "fitness challenges."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
            )
            text = response.choices[0].message.content.strip()
        except Exception:
            text = "Do 20 jumping jacks each day"

    text = clean_text(text)

    try:
        import json

        data = json.loads(text)
        return {
            "challenge_text": data.get("challenge_text", text),
            "days": int(data.get("days", 7)),
            "tone": tone,
        }
    except Exception:
        return {"challenge_text": text, "days": 7, "tone": tone}
