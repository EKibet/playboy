import json

import pytest
from django.core import mail

from MAT.apps.common.tasks import send_email_utility


class TestCeleryUtilityEmail():
    @pytest.mark.django_db
    def test_celery_utility_email_succeeds(self, client):
        kwargs = {"recipient_email":"test@gmail.com","subject":"Test Sendgrid","template":"student_invite_template.html","cc_recipients":None,"template_variables": {
                    'username': "student_name",
                    'attendance': "100%",
                }}
        send_email_utility(**kwargs)
        assert len(mail.outbox) == 1
