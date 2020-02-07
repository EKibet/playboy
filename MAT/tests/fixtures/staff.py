import pytest

# Models
from MAT.apps.staff.models import User, Staff


@pytest.fixture(scope='module')
def new_staff():
    params = {
        "first_name": "chris",
        "last_name": "karimi",
        "email":"chris@moringaschool.com",
        "username":"chris",
        "gender": "Female",
        "role": "Technical Mentor",
        "phone_number":"0716491250"

    }
    return Staff(**params)