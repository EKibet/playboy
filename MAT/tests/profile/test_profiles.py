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
            user_id=User.objects.get(email="testyy@mail.com"))
        response = client.get(url)
        assert response.data['data'].get('username') == 'Batman1'
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
    def test_edit_other_persons_profile(self, client, profile_token, new_user_with_profile2):
        """Test to edit the profile of another user"""
        new_user_with_profile2.save()
        update_data = {"gender": "female"}
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': new_user_with_profile2.user.id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.put(url, data=json.dumps(update_data),
                              content_type='application/json')
        assert response.data.get(
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

    
    @pytest.mark.django_db
    def test_only_pod_leader_can_upload_track(self, client, update_tracks_data,get_or_create_admin_token, get_or_create_token):
        student_token = get_or_create_token
        pod_leader_token = get_or_create_admin_token

        message_response = "You do not have permission to perform this action."
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + student_token)
        headers = {
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=file','HTTP_CONTENT_TYPE':'text/plain'
        }
        response = client.patch(
            reverse('profiles:update_tracks'), update_tracks_data, **headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data.get("detail") == message_response

    @pytest.mark.django_db
    def test_upload_track_fails_with_bad_csv(self, client, update_track_wrong_format,get_or_create_admin_token):
        """ test that update track fails with bad csv file """

        token = get_or_create_admin_token

        # message_response = "You need to upload a csv file to update."
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        headers = {
            'HTTP_CONTENT_DISPOSITION': 'attachment;filename=file','HTTP_CONTENT_TYPE':'text/csv'
        }
        # n/b file data contains 
        response = client.patch(
            reverse('profiles:update_tracks'), update_track_wrong_format, **headers)
        
        message_response = 'CSV data does not have correct format.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == message_response

