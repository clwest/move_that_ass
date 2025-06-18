from django.urls import path
from .views import upload_voice_journal

urlpatterns = [
    path("upload/", upload_voice_journal),
]
