import pytest
import rest_framework

pytest_plugins = ("MAT.tests.fixtures.users",
                  "MAT.tests.fixtures.cohort_and_students",
                  "MAT.tests.fixtures.staff", "MAT.tests.fixtures.students_list",)


@pytest.fixture(scope='function')
def client():
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Django rest framework API client
    """

    from rest_framework.test import APIClient
    return APIClient()
