import pytest

# Models
from MAT.apps.profiles.models import User
from MAT.apps.profiles.models import UserProfile

@pytest.fixture(scope='module')
def new_user():
    params = {
        "username": "sly",
        "email": "sly@gmail.com",
        "password": "sly123"
    }
    return User(**params)


@pytest.fixture(scope='function')
def new_user_with_profile(django_db_blocker, new_user):
    new_user.save()
    with django_db_blocker.unblock():
        params = {
            "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiro",
            "gender": "Male",
            "student_class": "MC21",
            "fullname": "MC21",
            "user": new_user
        }
        return UserProfile(**params)

