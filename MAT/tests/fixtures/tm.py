import pytest
from MAT.apps.authentication.models import Tm


@pytest.fixture(scope='function')
def new_tm():
    student = Tm.objects.create(first_name="first", last_name="last",
                                username="userjina", email='hey@mail.com', password='secret')
    return student
