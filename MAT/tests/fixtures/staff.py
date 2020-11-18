import pytest

# Models
from MAT.apps.authentication.models import User


@pytest.fixture(scope='function')
def new_staff():
    params = {
        "first_name": "chris",
        "last_name": "karimi",
        "email": "chris@moringaschool.com",
        "username": "chris"
    }
    return User(**params)
