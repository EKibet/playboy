import json
import pytest
from django.urls import reverse
from django.core import mail
from rest_framework import status
from MAT.apps.authentication.models import User

class TestSendEmails():
    """Tests for sending an email endpoint"""

    @pytest.mark.django_db
    def test_send_single_email_successfully(self, client, new_user, get_or_create_token):
        """Test for sending a single email successfully"""
        new_user.save()
        token = get_or_create_token
        url = reverse('staff:send-mail')
        data = {
            "recipients": ["sly@gmail.com"],
	        "subject": "Testing2",
	        "message": "Trying this out",
	        "sender": "sly@gmail.com"
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert (len(mail.outbox), 1)
        assert mail.outbox[0].subject, 'Testing2'
        assert mail.outbox[0].message, 'Trying this out'

    @pytest.mark.django_db
    def test_send_multiple_emails_successfully(self, client, new_user, new_user2,get_or_create_token):
        """Test for sending a single email successfully"""
        new_user.save()
        new_user2.save()
        token = get_or_create_token
        url = reverse('staff:send-mail')
        data = {
            "recipients": ["sly@gmail.com", "ken@gmail.com"],
	        "subject": "Testing2",
	        "message": "Trying this out",
	        "sender": "sly@gmail.com"
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert (len(mail.outbox), 1)
        assert mail.outbox[0].subject, 'Testing2'
        assert mail.outbox[0].message, 'Trying this out'

    @pytest.mark.django_db
    def test_send_unsuccessful_email(self, client, new_user,get_or_create_token):
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
        response = client.post(url, data=json.dumps(post_data), content_type='application/json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'There were no emails sent. Confirm that the right emails were input.'
        assert (len(mail.outbox), 0)
