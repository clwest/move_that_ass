from django.urls import path
from .views import identify_image

urlpatterns = [
    path("identify/", identify_image),
]
