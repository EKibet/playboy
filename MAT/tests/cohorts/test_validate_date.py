import pytest, json
from django.urls import reverse
from rest_framework import status
from MAT.apps.cohorts.models import Cohort

class TestCohortValidDate():
    @pytest.mark.django_db
    def test_validate_end_date(self, client, get_or_create_podleader_token):
        data = {
            "cohort_name": "MC22",
            "start_date" :"2020-11-11",
            "end_date" :"2020-12-11"
        }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED


    @pytest.mark.django_db
    def test_end_date_is_not_less_or_equal_to_start_date(self, client, get_or_create_podleader_token):
        data = {
                "cohort_name": "MC298",
                "start_date" :"2020-11-11",
                "end_date" :"2020-10-11"
            }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        exception = json.loads(response.content.decode())
        message = exception.get('cohort').get('end_date')[0]
        assert message == 'The end date cannot be same or before the start date.'

    @pytest.mark.django_db
    def test_start_date_is_required_when_end_date_is_present(self, client, get_or_create_podleader_token):
        data = {
                "cohort_name": "MC298",
                "end_date" :"2020-10-11"
            }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        exception = json.loads(response.content.decode())
        message = exception.get('cohort').get('end_date')[0]
        assert message == 'Please provide a start date'