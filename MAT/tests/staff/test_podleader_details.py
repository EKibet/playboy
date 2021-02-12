import json, pytest
from django.urls import reverse
from rest_framework import status


class TestPodLeaderDetails():

    @pytest.mark.django_db
    def test_get_podleader_details(self, client, get_or_create_admin_token, pod_leader2):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
        pod_leader2.save()
        url=reverse('staff:podleader-details', kwargs={'id':pod_leader2.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('deleted')==False

    @pytest.mark.django_db   
    def test_deleted_object_is_not_queried(self, client, pod_leader2, get_or_create_admin_token):
        '''
            This test asserts that an endpoint raises a 404 error if the queried object is marked as deleted
        '''
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
        pod_leader2.deleted =True
        pod_leader2.save()  
        url=reverse('staff:podleader-details', kwargs={'id':pod_leader2.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_podleader_details(self, client, pod_leader2, get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        pod_leader2.save()
        url = reverse('staff:podleader-details', kwargs={'id':pod_leader2.id})
        response = client.put(url, data = json.dumps({'first_name': 'Ktn'}), content_type = 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == 'Ktn'

    @pytest.mark.django_db
    def test_update_podleader_details_fails(self, client, pod_leader2, get_or_create_token):
        '''
            This test asserts that an update cannot be done with none admin users.
            The token provided here is for a student
        '''
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        pod_leader2.save()
        url = reverse('staff:podleader-details', kwargs={'id':pod_leader2.id})
        response = client.put(url, data = json.dumps({'first_name': 'Ktn'}), content_type = 'application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data.get('first_name') != 'Ktn'
        

    @pytest.mark.django_db
    def test_delete_podleader(self, client, pod_leader2, get_or_create_admin_token):
        '''
             This functions tests if the soft-delete is implemented. And check that the call to the endpoint with a deleted credential raises a 404 error.
        '''
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        pod_leader2.save()
        url = reverse('staff:podleader-details', kwargs={'id':pod_leader2.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == f'{pod_leader2.username} deleted successfully!'
        # Try accessing the same endpoind should raise a 404
        assert client.get(url).status_code == status.HTTP_404_NOT_FOUND