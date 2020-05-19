import pytest

from MAT.apps.authentication.models import User
from django.contrib.auth.hashers import make_password


@pytest.fixture(scope='function')
def new_student():
    student = User.objects.create_student(first_name="dave", last_name="kahara",
				username="Batman", email='test@mail.com', password='secret',cohort="mc23")
    return student


