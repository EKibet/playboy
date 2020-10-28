import json

import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status

import MAT.apps.staff.views
from MAT.apps.authentication.models import User


class TestSendEmails():
    """Tests for sending an email endpoint"""

    @pytest.mark.django_db
    def test_send_single_email_successfully(self, client, new_user, get_or_create_token, monkeypatch):
        """Test for sending a single email successfully"""
        new_user.save()
        token = get_or_create_token
        url = reverse('staff:send-mail')
        data = {
            "recipients": ["testyy@mail.com"],
            "subject": "Testing2",
            "message": "Trying this out",
            "sender": "test@mail.com"
        }

        self.celery_send_link_called = False

        def fake_trigger_celery_send_link(email, subject, template, url, token):
            self.celery_send_link_called = True
            self.subject = subject
            self.template = template
            self.email = email
            self.url = url
            self.token = token

        monkeypatch.setattr(MAT.apps.staff.views.celery_send_link,
                            "delay", fake_trigger_celery_send_link)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(
            data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert self.celery_send_link_called
        assert self.subject == 'Testing2'
        assert self.email == 'testyy@mail.com'

    @pytest.mark.django_db
    def test_send_multiple_emails_successfully(self, client, new_user, new_student, get_or_create_token, monkeypatch):
        """Test for sending a single email successfully"""
        new_user.save()
        new_student.save()
        token = get_or_create_token
        url = reverse('staff:send-mail')
        data = {
            "recipients": ["testyy@mail.com"],
            "subject": "Testing2",
            "message": "Trying this out",
            "sender": "test@gmail.com"
        }

        self.celery_send_link_called = False

        def fake_trigger_celery_send_link(email, subject, template, url, token):
            self.celery_send_link_called = True
            self.subject = subject
            self.template = template
            self.email = email
            self.url = url
            self.token = token

        monkeypatch.setattr(MAT.apps.staff.views.celery_send_link,
                            "delay", fake_trigger_celery_send_link)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(
            data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert "emails were successfully sent." in response.data["success"]
        assert self.celery_send_link_called
        assert self.subject == 'Testing2'
        assert self.email == 'testyy@mail.com'

    @pytest.mark.django_db
    def test_send_unsuccessful_email(self, client, new_user, get_or_create_token):
        """Test for sending an unsuccessful email"""
        new_user.save()
        token = get_or_create_token
        url = reverse('staff:send-mail')
        post_data = {
            "recipients": ["sly@hotmail.com"],
            "subject": "Testing2",
            "message": "Trying this out",
            "sender": "sly@hotmail.com"
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(
            post_data), content_type='application/json')
        assert len(mail.outbox) == 0
