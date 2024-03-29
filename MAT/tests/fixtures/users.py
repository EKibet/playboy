import json
from datetime import datetime, timedelta
from django.db import models

import jwt
import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse

# Models
from MAT.apps.authentication.models import Tm, Student, PodLeader, User
from MAT.apps.profiles.models import StudentProfile, StudentCurrentTrack
from MAT.config.settings.base import env

class Types(models.TextChoices):
        """User types"""
        TM = "TM", "Tm"
        STUDENT = "STUDENT", "Student"
        POD_LEADER = "POD_LEADER", "PodLeader"
        ADMIN = "ADMIN", "Admin"

@pytest.fixture(scope='function')
def new_user():
    student = Student.objects.create(first_name="dave", last_name="kahara",
				username="Batman1", email='testyy@mail.com', password='secret')
    return student

@pytest.fixture(scope='function')
def new_user2():
    params = {
        "username": "ken",
        "email": "ken@gmail.com",
        "password": make_password('ken'),
        "is_active": "True",
        "type": "STUDENT"
    }
    return User(**params)

@pytest.fixture(scope='function')
def new_user3():
    student = Student.objects.create(first_name="dave", last_name="kahara",
				username="Batman2", email='testy@mail.com', password='secret')
    student.is_verified = True
    return student
    
@pytest.fixture(scope='module')
def pod_leader():
    params = {
        "username": "podleader",
        "email": "podleader@mail.com",
        "password": make_password('test'),
        "is_active": 'True',
        "is_staff" : 'False',#changed this to false
    }
    return User(**params)

@pytest.fixture(scope='function')
def pod_leader2():
    pod_leader = PodLeader.objects.create(
        first_name="pod", 
        last_name="leader",
        username="kiongozi", 
        email='pod@mail.com', 
        password='secret')
    return pod_leader
    
@pytest.fixture
def get_or_create_podleader_token(db, client, pod_leader):
    pod_leader.type ='POD_LEADER'
    pod_leader.save()
    url = reverse('authentication:token_obtain_pair')
    my_data =  {
        "email": "podleader@mail.com",
        "password": "test"
	}
    response = client.post(url,data=json.dumps(my_data),
                                   content_type='application/json')
    token =  response.data['access']
    return token
    
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
            "user": new_user
        }
        return StudentProfile(**params)



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
        return StudentProfile(**params)

@pytest.fixture
def get_or_create_token(db,client,new_student):
    new_student.save()
    url = reverse('authentication:token_obtain_pair')
    my_data =  {
        "email": "test@mail.com",
        "password": "secret"
	}
    response = client.post(url,data=json.dumps(my_data),
                                   content_type='application/json')
    token =  response.data['access']
    return token

@pytest.fixture
def profile_token(db,client,new_user):
    new_user.save()
    url = reverse('authentication:token_obtain_pair')
    my_data =  {
        "email": "testyy@mail.com",
        "password": "secret"
	}
    response = client.post(url,data=json.dumps(my_data),
                                   content_type='application/json')
    token =  response.data['access']
    user_id = new_user.id
    return token, user_id

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


@pytest.fixture(scope='function')
def create_prep_track():
    track = StudentCurrentTrack.objects.create(track="javscript")
    return track

@pytest.fixture(scope='function')
def create_core_track():
    track = StudentCurrentTrack.objects.create(track="flask")
    return track
