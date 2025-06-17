from openai import OpenAI
from dotenv import load_dotenv
import json

from . import clean_text

load_dotenv()
try:
    client = OpenAI()
except Exception:
    client = None


def generate_meal_plan(goal: str, tone: str = "supportive", mood: str | None = None):
    """Generate a simple day meal plan using OpenAI."""
    goal_text = goal or "general health"

    tone_map = {
        "supportive": "Write with encouragement and positivity.",
        "strict": "Use a disciplined, no-nonsense style.",
        "donkey": "Inject donkey-themed humor and mild insults.",
    }
    tone_instructions = tone_map.get(tone, "Use a friendly tone.")

    mood_text = f" The user is feeling {mood}." if mood else ""

    prompt = (
        f"Create a one-day meal plan for someone with a '{goal_text}' goal."\
        f" {tone_instructions}{mood_text} "
        "Return JSON with keys breakfast, lunch, dinner, and snacks (list)."
    )


    if client is None:
        text = "{}"
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a nutrition coach crafting concise meal plans.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
            )
            text = response.choices[0].message.content.strip()
        except Exception:
            text = "{}"

    text = clean_text(text)

    try:
        return json.loads(text)
    except Exception:
        return {"raw": text}
