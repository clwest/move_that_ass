from django.urls import path

from .views import transcribe_voice

urlpatterns = [
    path("transcribe/", transcribe_voice),
]
