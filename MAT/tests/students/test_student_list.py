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

    @pytest.mark.django_db
    def test_student_detail_view(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_student.save()
        url = reverse('students:student_details', kwargs={
                      'email': 'test_user@gmail.com'})

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('email') == new_student.email

    @pytest.mark.django_db
    def test_throws_error_if_student_does_not_exist(self, client, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:student_details',kwargs={'email':'test_user@gmail.com'})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_can_update_student_details(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data={
            'email':'new_email@gmail.com'
        }
        new_student.save()
        url=reverse('students:student_details',kwargs={'email':'test_user@gmail.com'})
        response = client.put(url,data=data)
        assert response.status_code==status.HTTP_200_OK
        assert response.data.get('email') == 'new_email@gmail.com'
    
    @pytest.mark.django_db
    def test_throws_error_for_unexisting_student_details(self, client, new_student, get_or_create_token):
        data={
            'email':'new_email@gmail.com'
        }
        new_student.save()
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url=reverse('students:student_details',kwargs={'email':'inexistent_user@gmail.com'})
        response = client.put(url,data=data)
        assert response.status_code==status.HTTP_404_NOT_FOUND
        assert response.data.get('error') == "User does not exist."

