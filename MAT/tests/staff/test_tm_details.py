import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import CohortMembership


class TestTmDetails():
    """
    Test for getting tm profile information
    """

    @pytest.mark.django_db
    def test_get_single_tm_details_succeeds(self, client, new_tm, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_tm.save()
        url = reverse('staff:tm_details', kwargs={'id': new_tm.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == new_tm.first_name
        assert response.data.get('current_cohorts') == []

    @pytest.mark.django_db
    def test_get_single_tm_details_with_cohort_succeeds(self, client, new_tm, new_cohort, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_tm.save()
        new_cohort.save()
        membership = CohortMembership(
            user=new_tm, cohort=new_cohort, current_cohort=True)
        membership.save()
        url = reverse('staff:tm_details', kwargs={'id': new_tm.id})
        response = client.get(url)
        cohort_data = dict(response.data.get('current_cohorts')[0])
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == new_tm.first_name
        assert cohort_data['cohort_name'] == new_cohort.cohort_name

    @pytest.mark.django_db
    def test_non_existent_tm_details_fails(self, client, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('staff:tm_details', kwargs={'id': '0'})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_tm_profile_details_succeeds(self, client, new_tm, new_cohort, get_or_create_token):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_cohort.save()
        new_tm.save()
        membership = CohortMembership(
            user=new_tm, cohort=new_cohort, current_cohort=True)
        membership.save()
        url = reverse('staff:tm_details', kwargs={'id': new_tm.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == new_tm.first_name
        assert response.data.get('username') == new_tm.username

    @pytest.mark.django_db
    def test_delete_tm_succeeds(self, client, get_or_create_token, new_tm):
        """
        Test deletion of an existing tm

        """
        new_tm.save()
        token = get_or_create_token
        url = reverse('staff:tm_details', kwargs={'id': new_tm.id})

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.delete(url, content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_update_tm_details_succeeds(self, client, new_tm, get_or_create_token):
        """
            Test update single tm
        """
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'first_name': 'Newjina',
            'email': 'newemail@gmail.com'
        }
        new_tm.save()
        url = reverse('staff:tm_details', kwargs={'id': new_tm.id})
        response = client.patch(url, data=json.dumps(data),
                                content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('first_name') == 'Newjina'
        assert response.data.get('email') == new_tm.email
