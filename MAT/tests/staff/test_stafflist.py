import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User
from MAT.apps.staff.models import Staff


class TestStaffListing():
    @pytest.mark.django_db
    def test_get_allstaff(self, client,get_or_create_token):
        url = reverse('staff:stafflist')
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

class TestStaffCount():
    @pytest.mark.django_db
    def test_staff_count(self, new_staff):
        new_staff.save()
        assert Staff.objects.count() == 1



