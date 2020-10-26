import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User


class TestStaffDetails():
    """
    Test for listing single staff information
    """

    @pytest.mark.django_db
    def test_single_staff_details(self, client, new_admin_user, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_admin_user.save()
        url = reverse('staff:staff_details', kwargs={'id':new_admin_user.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == new_admin_user.first_name

    @pytest.mark.django_db
    def test_non_existent_staff_details(self, client, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('staff:staff_details', kwargs={'id':'2345'})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    @pytest.mark.django_db
    def test_update_staff_details(self, client, new_admin_user, get_or_create_token):
        """
            Test update single staff
        """
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data={
            'first_name':'Dababy',
            'email':'chris@gmail.com'
        }
        new_admin_user.save()
        url=reverse('staff:staff_details',kwargs={'id':new_admin_user.id})
        response = client.patch(url,data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code==status.HTTP_200_OK
        assert response.data.get('first_name') == 'Dababy'      


    @pytest.mark.django_db
    def test_delete_staff_succeeds(self, client, get_or_create_token, new_admin_user):
        """
        Test deletion of an existing staff
        
        """
        new_admin_user.save()
        token = get_or_create_token
        url=reverse('staff:staff_details',kwargs={'id':new_admin_user.id})

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.delete(url, content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT 
    
