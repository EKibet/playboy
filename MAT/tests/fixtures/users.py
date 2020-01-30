import pytest

# Models
from MAT.apps.authentication.models import User

@pytest.fixture(scope='function')
def new_user():
    params = {
        "username": "sly",
        "email": "sly@gmail.com",
        "password": "sly123"
    }
    return User(**params)

@pytest.fixture(scope='function')
def new_user_without_username():
    params = {
        "username": None,
        "email": "sly@gmail.com",
        "password": "sly123"
    }
    return params
