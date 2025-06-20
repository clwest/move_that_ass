import requests
import os
from django.conf import settings

ELEVENLABS_API_KEY = settings.ELEVENLABS_API_KEY
VOICE_ID = settings.VOICE_ID


def text_to_speech(text, output_path="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.6},
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    return None
