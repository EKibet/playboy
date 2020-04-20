import pytest
import json

from rest_framework import status
from django.urls import reverse
from MAT.apps.authentication.models import User

class TestRegistration:

    @pytest.mark.django_db
    def test_cannot_register_user_without_token(self,new_user, client):
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"admin@gmail.com",
                                "password":"12345"}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_cannot_register_user_with_valid_token_but_not_admin(self,get_or_create_token, client):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"admin@gmail.com",
                                "password":"12345"}, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_successful_registration_with_valid_token_and_staff_role(self,get_or_create_admin_token, client):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('authentication:SingleUserRegistration')

        user = {
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"admin@gmail.com",
                                "password":"12345",
                                "role":"staff"
    }


        response = client.post(url,data=json.dumps(user),content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_successful_registration_with_valid_token_and_student_role(self,get_or_create_admin_token, client):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('authentication:SingleUserRegistration')

        user = {
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"admin@gmail.com",
                                "password":"12345",
                                "role":"student"
    }


        response = client.post(url,data=json.dumps(user),content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_user_registration_fails_without_password(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"admin@gmail.com",
                                "password":""}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_without_email(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"chris",
                                "email":"",
                                "password":"xicnrire"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_with_wrong_email_format(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "jdnwod",
                                "last_name": "cdncwoer",
                                "username":"kjnf",
                                "email":"admingmail.com",
                                "password":"xsxwxwe"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_with_password_length_below_four(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "jdnwod",
                                "last_name": "cdncwoer",
                                "username":"kjnf",
                                "email":"admingmail.com",
                                "password":"xsxwxwe"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_without_username(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "chris",
                                "last_name": "karimi",
                                "username":"",
                                "email":"admin@gmail.com",
                                "password":"xsxwxwe"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_without_firstname(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "",
                                "last_name": "karimi",
                                "username":"kjnf",
                                "email":"admin@gmail.com",
                                "password":"xsxwxwe"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_registration_fails_without_lasttname(self, client, new_user, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(reverse('authentication:SingleUserRegistration'),{
                                "first_name": "jdnwod",
                                "last_name": "",
                                "username":"kjnf",
                                "email":"admin@gmail.com",
                                "password":"xsxwxwe"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
