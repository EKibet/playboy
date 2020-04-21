import json

import pytest
from django.core import mail

from MAT.apps.staff.tasks import celery_send_link


class TestCeleryEmail():
    @pytest.mark.django_db
    def test_celery_email_succeeds(self, client):
        
        kwargs = {"email":"starfordomwakwe@gmail.com", "subject":"subject", \
            "template":"student_invite_template.html", "url":"url", "token":"token"}
        celery_send_link(**kwargs)
        print("len(mail.outbox) ", len(mail.outbox))
        assert len(mail.outbox) == 1
