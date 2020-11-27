import pytest

from MAT.apps.cohorts.models import Cohort


@pytest.fixture(scope='function')
def new_cohort():
    params = {
        "name": "MC01",
        "start_date": "2020-11-20"
    }
    return Cohort(**params)
