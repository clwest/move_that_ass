from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("api/core/", include("core.urls")),
    path("api/shame/", include("shame.urls")),
    path("api/voice/", include("voice_journals.urls")),
    path("api/prompts/", include("prompts.urls")),
    path("api/content/", include("content.urls")),
    path("api/movement/", include("movement.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
