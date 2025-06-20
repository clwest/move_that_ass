import base64
import requests
from celery import shared_task
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def identify_image_task(self, task_id: str, image_path: str):
    """Identify the image using OpenAI Vision or Gemini."""
    label = "unknown"
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Identify the primary subject"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{data}"}},
                    ],
                }
            ],
            "max_tokens": 5,
        }
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        res = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=20)
        label = res.json()["choices"][0]["message"]["content"].strip().split("\n")[0]
    except Exception:
        pass
    is_dangerous = label.lower() in [
        "rattlesnake",
        "cobra",
        "mountain lion",
        "poison ivy",
    ]
    wiki_url = ""
    try:
        wiki_res = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{label}", timeout=10
        )
        wiki_data = wiki_res.json()
        wiki_url = wiki_data.get("content_urls", {}).get("desktop", {}).get("page", "")
    except Exception:
        pass

    return {"label": label, "is_dangerous": is_dangerous, "wiki_url": wiki_url}
