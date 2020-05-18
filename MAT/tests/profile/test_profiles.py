import json

import pytest
from django.urls import reverse
from rest_framework import status

import MAT.apps.common.utility
import MAT.apps.profiles.views
from MAT.apps.authentication.models import User
from MAT.apps.common.utility import make_cloudinary_url
from MAT.config.settings.base import BASE_DIR
from MAT.apps.students.models import AttendanceRecords


class TestUserProfile():
    """Tests for the user profile endpoint"""

    @pytest.mark.django_db
    def test_get_all_profiles(self, client, get_or_create_token):
        """Test for getting a all profiles"""
        token = get_or_create_token
        url = reverse('profiles:all_profiles')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existant_profile(self, get_or_create_token, client):
        """Test fetch non-existant profile on registration """
        token = get_or_create_token
        url = reverse('profiles:profile_details', kwargs={'id': '123'})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_user_profile(self, client, profile_token):
        """Test fetch existant profile on registration """
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': user_id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        AttendanceRecords.objects.create(
            user_id=User.objects.get(email="sly@gmail.com"))
        response = client.get(url)
        assert response.data['data'].get('username') == 'sly'
        assert response.data['data'].get('student_class') == 'MC21'
        assert response.data['data'].get('gender') == 'Male'
        assert response.data['attendance'].get('attendance_percentage') == 0.0
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_edit_user_profile(self, client, profile_token):
        """Test edit existant profile on registration """
        update_data = {"gender": "female"}
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': user_id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.put(url, data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('gender') == 'female'

    @pytest.mark.django_db
    def test_edit_other_persons_profile(self, client, profile_token, new_user2):
        """Test to edit the profile of another user"""
        new_user2.save()
        update_data = {"gender": "female"}
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': new_user2.id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.put(url, data=json.dumps(update_data),
                              content_type='application/json')
        response.data.get(
            'error') == 'You are not allowed to edit another persons profile'
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_user_profile_picture_succeeds(self, client, profile_token, monkeypatch):
        """Test edit profile picture of an existing profile"""
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': user_id})
        self.make_cloudinary_url_called = False

        def fake_make_cloudinary_url(profile_picture, username):
            self.make_cloudinary_url_called = True
            self.username = username
            # return an example url from make_cloudinary_url function
            return 'https://res.cloudinary.com/cloudname/image/upload/v1588683070/test/mock.png'

        monkeypatch.setattr(MAT.apps.profiles.views,
                            "make_cloudinary_url", fake_make_cloudinary_url)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        with open('MAT/tests/profile/sample_picture.png', "rb") as fp:
            response = client.put(url, data={'profile_picture': fp}, )
        assert response.status_code == status.HTTP_200_OK
        assert self.make_cloudinary_url_called

    def test_upload_image_to_cloudinary_succeeds(self, monkeypatch):
        """Test make_cloudinary_url takes in an image and returns a cloudinary url"""
        self.upload_called = False

        def fake_upload(image, folder="CLOUDINARY_FOLDER", public_id="username", overwrite=True):
            self.upload_called = True
            # return a mock response from cloudinary
            cloudinary_mock_response = {'public_id': 'public-id',
                                        'secure_url': 'http://sample.com/mock.png',
                                        }
            return cloudinary_mock_response

        monkeypatch.setattr(MAT.apps.common.utility,
                            "upload", fake_upload)

        with open('MAT/tests/profile/sample_picture.png', "rb") as fp:
            cloudinary_url = make_cloudinary_url(fp, "mock_username")

            assert self.upload_called
            assert cloudinary_url == 'http://sample.com/mock.png'
