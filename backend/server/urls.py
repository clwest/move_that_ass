from django.contrib import admin
from django.urls import include, path
from voice_journals.views import upload_voice_journal
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("accounts.urls")),
    path(
        "api/core/upload-voice/",
        upload_voice_journal,
    ),
    path("api/core/", include("core.urls")),
    path("api/core/", include("shame.urls")),
    path("api/voice/", include("voice_journals.urls")),
    path("api/prompts/", include("prompts.urls")),
    path("api/content/", include("content.urls")),
    path("api/movement/", include("movement.urls")),
    path("api/vision/", include("vision.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
