import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User


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
        response = client.get(url)
        assert response.data.get('username') == 'sly'
        assert response.data.get('student_class') == 'MC21'
        assert response.data.get('gender') == 'Male'
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_edit_user_profile(self, client, profile_token):
        """Test edit existant profile on registration """
        update_data = {"gender":"female"}
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
        update_data = {"gender":"female"}
        token, user_id = profile_token
        url = reverse('profiles:profile_details', kwargs={'id': new_user2.id})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.put(url, data=json.dumps(update_data),
                              content_type='application/json')
        response.data.get('error') == 'You are not allowed to edit another persons profile'
        assert response.status_code == status.HTTP_403_FORBIDDEN