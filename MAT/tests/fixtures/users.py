import json
from datetime import datetime, timedelta

import jwt
import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse

# Models
from MAT.apps.profiles.models import User, UserProfile
from MAT.config.settings.base import env

@pytest.fixture(scope='module')
def new_user():
    params = {
        "username": "sly",
        "email": "sly@gmail.com",
        "password": make_password('sly123'),
        "is_student":True,
        "is_verified":True
    }
    return User(**params)

@pytest.fixture(scope='module')
def new_user2():
    params = {
        "username": "ken",
        "email": "ken@gmail.com",
        "password": make_password('ken'),
        "is_active": "True"
    }
    return User(**params)
@pytest.fixture(scope='function')
def new_admin_user(django_db_blocker):
    with django_db_blocker.unblock():
        params = {
        "username": "whack",
        "email": "whack@gmail.com",
        "password": make_password('whacker'),
        }
        admin=User(**params)
        admin.is_superuser=True
        admin.is_staff=True
        admin.save()
        return admin


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



@pytest.fixture(scope='function')
def new_user_with_profile2(django_db_blocker, new_user2):
    new_user2.save()
    with django_db_blocker.unblock():
        params = {
            "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiro",
            "gender": "Male",
            "student_class": "MC21",
            "fullname": "MC21",
            "user": new_user2
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

@pytest.fixture(scope='function')
def get_or_create_admin_token(db,client,new_admin_user):
    new_admin_user.save()
    url = reverse('authentication:token_obtain_pair')
    my_data =  {
        "email": "whack@gmail.com",
        "password": "whacker"
	}
    response = client.post(url,data=json.dumps(my_data),
                                   content_type='application/json')
    token =  response.data['access']
    return token

@pytest.fixture(scope='function')
def create_expired_token(db, new_user):
    user = new_user.save()
    JWT_SECRET = env.str('SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_DAYS = 60

    payload = {
        'user_id': 2,
        'exp': datetime.utcnow() - timedelta(days=JWT_EXP_DELTA_DAYS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token
