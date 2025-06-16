from rest_framework.routers import DefaultRouter
from .views import PromptViewSet, PromptResponseViewSet

router = DefaultRouter()
router.register(r'prompts', PromptViewSet)
router.register(r'responses', PromptResponseViewSet)

urlpatterns = router.urls
