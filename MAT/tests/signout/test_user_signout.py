import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User
from rest_framework.authtoken.models import Token


class TestLogout:
    """[Tests that logout functionality works]
    Given a valid refresh token, a new access token is generated.
    When a user logs out, the token is blacklisted and can not be used to 
    create a new access token
    """
    @pytest.mark.django_db
    def test_logout(self, new_user, client, get_or_create_token):
        token = get_or_create_token
        new_user.save()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        sign_in_response = client.post(reverse('authentication:token_obtain_pair'), {
                            "email": "testyy@mail.com", "password": "secret"}, format='json')
        assert sign_in_response.status_code == status.HTTP_200_OK
        refresh_token_response = client.post(reverse('authentication:token_refresh'), {
                    "refresh": sign_in_response.data.get('refresh')}, format='json')
        assert refresh_token_response.status_code == status.HTTP_200_OK

        sign_out_response = client.post(reverse('authentication:SignoutView'),{
        "refresh_token": sign_in_response.data.get('refresh')
        }, format='json')
        assert sign_out_response.status_code == status.HTTP_200_OK

        refresh_token_response = client.post(reverse('authentication:token_refresh'), {
                    "refresh": sign_in_response.data.get('refresh')}, format='json')
        assert refresh_token_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert refresh_token_response.data.get('detail') == "Token is blacklisted"

