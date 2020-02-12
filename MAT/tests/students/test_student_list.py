import collections

import pytest
from django.urls import reverse
from rest_framework import status

from MAT.apps.authentication.models import User


class TestStudentsList:
    """Test class for retrieving students"""
    @pytest.mark.django_db
    def test_get_students_list_ok(self, client,get_or_create_token):
        """Test for getting a students list status"""
        token = get_or_create_token
        url = reverse('students:list_students')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_students_list_type(self, client,get_or_create_token):
        """Test for getting a students list return type"""
        token = get_or_create_token
        url = reverse('students:list_students')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert True == isinstance(response.data, collections.OrderedDict)
