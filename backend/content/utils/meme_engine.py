import os
import random
import requests
from openai import OpenAI
from dotenv import load_dotenv
from core.utils import clean_text

load_dotenv()

GIPHY_KEY = os.getenv("GIPHY_API_KEY")
try:
    client = OpenAI()
except Exception:
    client = None

# Fallback donkey GIF if the GIPHY API call fails or no key is configured
DEFAULT_DONKEY_GIF = (
    "https://media.giphy.com/media/3ohzdFHDBEG32PmWJO/giphy.gif"
)


def fetch_donkey_gif():
    """Return a donkey-themed GIF URL from GIPHY."""
    url = "https://api.giphy.com/v1/gifs/search"
    params = {"api_key": GIPHY_KEY, "q": "donkey meme", "limit": 5}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        gifs = [d["images"]["original"]["url"] for d in data.get("data", [])]
        return random.choice(gifs) if gifs else DEFAULT_DONKEY_GIF
    except Exception:
        return DEFAULT_DONKEY_GIF


def generate_meme_caption(tone: str = "funny") -> str:
    """Generate a short caption for a donkey meme."""
    prompt = (
        f"Write a short, {tone} caption for a donkey meme about someone failing to exercise."
    )

    if client is None:
        return "keep moving!"
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You're a meme expert who writes funny captions.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
        )
        text = response.choices[0].message.content.strip()
    except Exception:
        text = "keep moving!"

    return clean_text(text)

