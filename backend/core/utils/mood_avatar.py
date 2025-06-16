MOOD_EMOJIS = {
    "ashamed": "😔🫏",
    "hype": "🔥🫏",
    "neutral": "😐🫏",
    "thoughtful": "🤔🫏",
    "annoyed": "😒🫏",
    "playful": "😜🫏",
    "burned out": "💀🫏",
}


def get_mood_avatar(mood):
    """Return the avatar (emoji) for a given mood."""
    return MOOD_EMOJIS.get(mood, "😐🫏")
