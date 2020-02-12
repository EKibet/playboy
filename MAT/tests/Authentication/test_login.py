import pytest
import json

from rest_framework import status
from django.urls import reverse
from MAT.apps.authentication.models import User


class TestLogin:
    @pytest.mark.django_db
    def test_can_login_with_correct_credentials(self,new_user, client):
        new_user.save()
        response = client.post(reverse('authentication:token_obtain_pair'), {
                            "email": "sly@gmail.com", "password": "sly123"}, format='json')
        assert response.status_code == status.HTTP_200_OK


    @pytest.mark.django_db
    def test_user_login_without_email(self, client, new_user):
        new_user.save()
        response = client.post(reverse('authentication:token_obtain_pair'), {
                            "email": "", "password": "sly123"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_login_without_password(self, client, new_user):
        new_user.save()
        response = client.post(reverse('authentication:token_obtain_pair'), {
                            "email": "sly@gmail.com", "password": ""}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_login_wrong_credentials(self, client, new_user):
        new_user.save()
        response = client.post(reverse('authentication:token_obtain_pair'), {
                            "email": "sly.com", "password": "123"}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
