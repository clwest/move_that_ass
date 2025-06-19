import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    res = client.post(reverse('accounts-register'), {"email": "a@example.com", "password": "secret"}, format='json')
    assert res.status_code == 201
    user = User.objects.get(email="a@example.com")
    assert not user.is_verified

    # mark verified for login
    user.is_verified = True
    user.save()
    res = client.post(reverse('accounts-login'), {"email": "a@example.com", "password": "secret"}, format='json')
    assert res.status_code == 200
    assert 'access' in res.data
    assert 'refresh' in res.data
