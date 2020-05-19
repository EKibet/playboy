from io import BytesIO

import pytest
from rest_framework.test import APIClient

from MAT.apps.authentication.models import User
from MAT.apps.students.models import AttendanceRecords
from MAT.config.settings.base import BASE_DIR
import os

@pytest.fixture
def change_time():
    check_out=os.environ.get('CHECKOUT_TIME')
    check_out='25:00:00'
    return check_out
@pytest.fixture(scope='module')
def file_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/test.csv'), 'rb')
    }

    return params
@pytest.fixture(scope="function")
def create_attendance_record(new_user):
    new_user.save()
    current_user=User.objects.get(email="testy@mail.com")
    return AttendanceRecords.objects.create(user_id=current_user)
