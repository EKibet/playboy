import pytest
import json

from rest_framework import status
from django.urls import reverse
from MAT.apps.authentication.models import User

class TestAssign:
    @pytest.mark.django_db
    def test_cannot_assign_if_not_admin(self,get_or_create_token,client):
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.patch(reverse('cohorts:assign-cohort'),{
            "cohort":"mc32",
            "list_of_tms":[
                "h@gmail.com",
                "m@gmail.com"
            ]
        }, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.django_db
    def test_successful_cohort_assignment_with_valid_token_and_admin_role(self,get_or_create_admin_token, client):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('cohorts:assign-cohort')
        user = {
            "cohort":"mc32",
            "list_of_tms":[
                "h@gmail.com",
                "m@gmail.com"
            ]
        }
        response = client.patch(url,data=json.dumps(user),content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
    