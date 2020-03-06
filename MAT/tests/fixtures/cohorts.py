import pytest

from MAT.apps.cohorts.models import Cohort


@pytest.fixture(scope='module')
def new_cohort():
    params = {
        "name": "mc01",
    }
    return Cohort(**params)
