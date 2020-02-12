import pytest
import json
from django.urls import reverse


# Models
from MAT.apps.profiles.models import User, UserProfile
from django.contrib.auth.hashers import make_password



@pytest.fixture(scope='module')
def new_user():
    params = {
        "username": "sly",
        "email": "sly@gmail.com",
        "password": make_password('sly123'),
        "is_active": "True"
    }
    return User(**params)

@pytest.fixture(scope='module')
def new_user2():
    params = {
        "username": "ken",
        "email": "ken@gmail.com",
        "password": "ken"
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
@pytest.fixture
def get_or_create_token(db,client,new_user):
    new_user.save()
    url = reverse('authentication:token_obtain_pair')
    my_data =  {
        "email": "sly@gmail.com",
        "password": "sly123"
	}
    response = client.post(url,data=json.dumps(my_data),
                                   content_type='application/json')
    token =  response.data['access']
    return token
