import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_profile_view():
    user = User.objects.create_user(email="b@example.com", password="pass", is_verified=True)
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    res = client.get("/api/core/profile/")
    assert res.status_code == 200
    assert res.data['user']['email'] == user.email
