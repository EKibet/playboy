import pytest

from MAT.apps.authentication.models import User
from django.contrib.auth.hashers import make_password


@pytest.fixture(scope='module')
def new_student():
        params = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "John",
            "password": make_password('sdssfdf'),
            "email": "test_user@gmail.com",
            "is_student": True

        }
        return User(**params)
