import os
from io import BytesIO

import pandas as pd
from MAT.config.settings import base
import pytest
from django.core import mail

from MAT.config.settings.base import BASE_DIR
from MAT.apps.authentication.models import CohortMembership


@pytest.fixture(autouse=True)
def sendgrid_backend_setup():
    base.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend' 


@pytest.fixture(autouse=True)
def email_backend_setup():
    base.EMAIL_HOST_PASSWORD = 'wrongapikey'       
@pytest.fixture(scope='function')
def wrong_file_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/final_list_wrong_data.csv'), 'rb')
    }

    return params
@pytest.fixture(scope='function')
def key_errored_related_file_data():
    params = {
        'file': open(BASE_DIR.path('MAT/tests/fixtures/final_list_sample_data_for_key_error.csv'), 'rb')
    }

    return params

    
@pytest.fixture(scope="function")
def cohort_membership():

    params = {
        "first_name": "Edgar",
        "last_name": "kibet",
        "email": "edgar.kibet@moringaschool.com",
        "username": "EKibet",
        "pasword":"cohort_membership",
        'cohort':"MPFT32",
        "role":"TM"
    }
    return CohortMembership(**params)

