import random
from django.utils import timezone
from ..models import DailyLockout, ShamePost


def generate_donkey_caption(user):
    captions = [
        f"{user.username} chose sloth over glory.",
        f"{user.username} is now eligible for the Couch Potato Championship.",
        f"No steps, no honor, {user.username}.",
        "The donkey saw your laziness. It wept.",
    ]
    return random.choice(captions)


def generate_donkey_image():
    # Replace later with image gen logic
    return "https://example.com/shameful_donkey_placeholder.jpg"


def check_and_trigger_shame(user):
    today = timezone.now().date()
    lockout = DailyLockout.objects.filter(user=user, date=today).first()
    if not lockout or lockout.is_unlocked:
        return None

    caption = generate_donkey_caption(user)
    image_url = generate_donkey_image()

    return ShamePost.objects.create(
        user=user,
        date=today,
        caption=caption,
        image_url=image_url,
        posted_to=[],
        was_triggered=True,
    )
