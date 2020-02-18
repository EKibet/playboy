import json
import pytest
from django.urls import reverse
from django.core import mail
from rest_framework import status
from MAT.apps.authentication.models import User


class TestSendEmails():
    """Tests for sending an email endpoint"""

    @pytest.mark.django_db
    def test_send_email_successfully(self, client, new_user, get_or_create_token):
        new_user.save()
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:SendPasswordResetEmail')
        data = {
            "email": "sly@gmail.com"
        }
        response = client.post(url, data=json.dumps(
            data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert len(mail.outbox) == 1


        token = response.data.get('token')
        url2 = reverse('students:ResetPasswordView', kwargs={'token': token})
        data2 = {
            "password": "test",
            "confirm_password": "test"
        }
        response = client.put(url2, data=json.dumps(
            data2), content_type="application/json")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_send_email_unsuccessful(self, client, get_or_create_token):

        url = reverse('students:SendPasswordResetEmail')
        data = {
            "email": "sly@mail.com"
        }
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(
            data), content_type='application/json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    @pytest.mark.django_db
    def test_password_does_match(self, client, new_user, get_or_create_token):

        new_user.save()
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:SendPasswordResetEmail')
        data = {
            "email": "sly@gmail.com"
        }
        response = client.post(url, data=json.dumps(
            data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert len(mail.outbox) == 1


        token = response.data.get('token')
        url2 = reverse('students:ResetPasswordView', kwargs={'token': token})
        data2 = {
            "password": "test",
            "confirm_password": "testy"
        }
        response = client.put(url2, data=json.dumps(
            data2), content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

