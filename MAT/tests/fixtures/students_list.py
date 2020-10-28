import pytest

from MAT.apps.authentication.models import Student
from django.contrib.auth.hashers import make_password


@pytest.fixture(scope='function')
def new_student():
    student = Student.objects.create(first_name="dave", last_name="kahara",
				username="Student1", email='test@mail.com', password='secret', is_verified=True)
    student.is_verified = True

    return student


