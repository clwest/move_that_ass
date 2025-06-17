from typing import Any


def generate_caption(description: str, tone: str = "funny") -> str:
    if tone == "funny":
        return f"When you're just trying to vibe but gravity wins. ({description})"
    elif tone == "poetic":
        return f"In the quiet stillness, {description} spoke to the soul."
    elif tone == "savage":
        return f"{description}? This is why the donkey weeps."
    elif tone == "encouraging":
        return f"You showed up. That's more than most. ({description})"
    return f"{description}, unfiltered."
