from io import BytesIO

import pytest
from rest_framework.test import APIClient

from MAT.apps.authentication.models import User, Student
from MAT.apps.students.models import AttendanceRecords
from MAT.config.settings.base import BASE_DIR
import os

@pytest.fixture
def change_time():
    check_out=os.environ.get('CHECKOUT_TIME')
    check_out='25:00:00'
    return check_out
@pytest.fixture(scope='function')
def file_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/final_list_sample_data.csv'), 'rb')
    }

    return params

@pytest.fixture(scope="function")
def create_attendance_record(new_user):
    new_user.save()
    current_user=Student.objects.get(email="test@mail.com")
    return AttendanceRecords.objects.create(user_id=current_user)

@pytest.fixture(scope='function')
def update_track_wrong_format():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/update_students_tracks.csv'), 'rb')
    }
    return params

@pytest.fixture(scope='function')
def update_tracks_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/update_students_tracks.csv'), 'rb')
    }
    return params