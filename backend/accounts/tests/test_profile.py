import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_profile_view():
    User.objects.all().delete()
    user = User.objects.create_user(
        username="bob", email="b@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    res = client.get("/api/core/profile/")
    assert res.status_code == 200
    assert res.data["user"]["email"] == user.email
    assert res.data["user"]["username"] == user.username


@pytest.mark.django_db
def test_profiles_requires_auth():
    client = APIClient()
    res = client.get("/api/core/profiles/")
    assert res.status_code == 401


@pytest.mark.django_db
def test_profiles_authenticated():
    User.objects.all().delete()
    user = User.objects.create_user(
        username="charlie", email="c@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    res = client.get("/api/core/profiles/")
    assert res.status_code == 200
