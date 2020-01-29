import pytest

from MAT.apps.students.models import Cohort, Students


@pytest.fixture(scope='module')
def new_student(django_db_blocker, new_cohort):
    new_cohort.save()
    with django_db_blocker.unblock():
        params = {
            "first_name": "John",
            "second_name": "Doe",
            "student_cohort": new_cohort,
            "username": "John",
            "password": "fggvbvvvb23",
            "email": "star@gmail.com"
        }
        return Students(**params)
