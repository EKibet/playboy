from io import BytesIO

import pytest
from rest_framework.test import APIClient

from MAT.apps.students.models import Cohort
from MAT.config.settings.base import BASE_DIR

@pytest.fixture(scope='module')
def new_cohort():
    params = {
        "name": "MC21",

    }
    return Cohort(**params)


@pytest.fixture(scope='module')
def file_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/test.csv'), 'rb')
    }

    return params
