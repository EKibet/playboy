import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User


class TestUserProfile():
    """Tests for the user profile endpoint"""

    @pytest.mark.django_db
    def test_get_all_profiles(self, client):
        """Test for getting a all profiles"""
        url = reverse('profiles:all_profiles')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existant_profile(self, client):
        """Test fetch non-existant profile on registration """
        url = reverse('profiles:profile_details', kwargs={'username': 'none'})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_user_profile(self, client,new_user):
        """Test fetch non-existant profile on registration """
        new_user.save()
        url = reverse('profiles:profile_details', kwargs={'username': 'sly'})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_edit_user_profile(self, client,new_user):
        """Test fetch non-existant profile on registration """
        update_data = {
            "profile": {
                "gender": "female"
            }}
        new_user.save()
        url = reverse('profiles:profile_details', kwargs={'username': 'sly'})
        response = client.put(url, data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == status.HTTP_200_OK




