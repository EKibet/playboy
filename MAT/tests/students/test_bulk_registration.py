import csv
# import
import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

class TestCohort:
    def test_can_create_cohort(self, client, db,get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(
            reverse('students:cohort-creation'), {"name": "MC231"}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_cannot_create_existing_cohort(self, client, db,get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        first_record = client.post(
            reverse('students:cohort-creation'), {"name": "MC231"}, format='json')
        response = client.post(
            reverse('students:cohort-creation'), {"name": "MC231"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_cohorts(self, client, db,get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(
            reverse('students:cohort-creation'), format='json')
        assert response.status_code == status.HTTP_200_OK


class TestStudentEndpoints:
    @pytest.mark.django_db
    def test_get_all_students(self, client,get_or_create_token):
        """Test for getting a all students in a cohort"""
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:list_create_students')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_post_csv_file(self, client, file_data,get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        headers = {
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=file','HTTP_CONTENT_TYPE':'text/plain'
        }
        response = client.post(
            reverse('students:list_create_students'), file_data, **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('error_count')  == 6
        assert response.data.get('created_count')  == 0
