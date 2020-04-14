import pytest
import json
import os
from django.urls import reverse


class TestOAuth2:
    def test_cannot_signup_or_login_with_invalid_token(self, client):
        url = reverse("authentication:social_auth")
        response = client.post(url, data={"token": "inavlid"})
        assert response.status_code == 401
    