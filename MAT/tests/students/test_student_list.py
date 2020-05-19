import collections

import pytest
from django.urls import reverse
from rest_framework import status

from MAT.apps.authentication.models import User


class TestStudentsList:
    """Test class for retrieving students"""
    @pytest.mark.django_db
    def test_get_students_list_ok(self, client, get_or_create_token):
        """Test for getting a students list status"""
        token = get_or_create_token
        url = reverse('students:list_students')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_students_list_type(self, client, get_or_create_token):
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
                      'email': 'test@mail.com'})

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('email') == new_student.email

    @pytest.mark.django_db
    def test_throws_error_if_student_does_not_exist(self, client, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:student_details', kwargs={
                      'email': 'siwezani@mail.com'})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_can_update_student_details(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'email': 'new_email@gmail.com'
        }
        new_student.save()
        url = reverse('students:student_details', kwargs={
                      'email': 'test@mail.com'})
        response = client.put(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('email') == 'new_email@gmail.com'

    @pytest.mark.django_db
    def test_throws_error_for_unexisting_student_details(self, client, new_student, get_or_create_token):
        data = {
            'email': 'new_email@gmail.com'
        }
        new_student.save()
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:student_details', kwargs={
                      'email': 'inexistent_user@gmail.com'})
        response = client.put(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data.get('error') == "User does not exist."

    @pytest.mark.django_db
    def test_verify_student_account(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_student.save()
        url = reverse('students:student_verification', kwargs={
                      'token': token})

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_error_decoding_token(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        token_2 = 'slkdlsdkslkdlskdsldkslkdlskdlskdksdklsdkdsl'
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:student_verification', kwargs={
                      'token': token_2})
        response = client.get(url)
        assert response.data.get(
            'detail') == "Error decoding token, please generate a new one."

    @pytest.mark.django_db
    def test_expired_token(self, client, new_student, get_or_create_token, create_expired_token):
        token = get_or_create_token
        token_2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1OTg0ODIyLCJqdGkiOiI4OWQwZjQ2NWFkNjU0NTYzOWJkZjRhZTNhODI1YTBkMSIsInVzZXJfaWQiOjF9.ik0Yat7Pi1_wCBhEx1weodGX6prglv3MQ1LRlyuMIOk'
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:student_verification', kwargs={
                      'token': create_expired_token})
        response = client.get(url)
        assert response.data.get(
            'detail') == "Error decoding token, please generate a new one."

    @pytest.mark.django_db
    def test_verify_student_account(self, client, new_student, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_student.save()
        url = reverse('students:student_verification', kwargs={
                      'token': token})

        client.get(url)
        response = client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
