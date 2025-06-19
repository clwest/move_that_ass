from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@shared_task
def send_verification_email(user_id: int):
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return
    token = RefreshToken.for_user(user)
    url = settings.FRONTEND_BASE_URL + "/verify/?token=" + str(token)
    msg = EmailMessage(
        subject="Verify your account",
        body=f"Click to verify: {url}",
        to=[user.email],
    )
    if getattr(settings, "CELERY_DISABLED", "0") == "1":
        msg.send(fail_silently=True)
    else:
        msg.send()
