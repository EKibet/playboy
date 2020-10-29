import csv

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status


class TestStudentEndpoints:
    @pytest.mark.django_db
    def test_get_all_students_succeeds(self, client,get_or_create_token):
        """Test for getting a all students in a cohort"""
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('students:list_students')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.skip(reason="no way of currently Mocking csv data")
    @pytest.mark.django_db
    def test_post_csv_file(self, client, file_data,get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        headers = {
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=file','HTTP_CONTENT_TYPE':'text/plain'
        }
        response = client.post(
            reverse('students:create_students'), file_data, **headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('error_count')  == 6
        assert response.data.get('created_count')  == 0


    def test_only_podleader_can_upload_csv(self, client, file_data, get_or_create_token, get_or_create_admin_token):
        """ Test podleader or admin can upload csv"""
        student_token = get_or_create_token
        pod_leader_token = get_or_create_admin_token

        message_response = "You do not have permission to perform this action."

        # test student upload
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ student_token)
        headers = {
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=file','HTTP_CONTENT_TYPE':'text/plain'
        }
        response = client.post(
            reverse('students:create_students'), file_data, **headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data.get("detail") == message_response

