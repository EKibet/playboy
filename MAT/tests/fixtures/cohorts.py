import pytest

from MAT.apps.cohorts.models import Cohort


@pytest.fixture(scope='function')
def new_cohort():
    params = {
        "cohort_name": "mc01",
    }
    return Cohort(**params)
