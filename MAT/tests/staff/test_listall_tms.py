import json
import pytest
from django.urls import reverse
from rest_framework import status
from MAT.apps.authentication.models import User,Tm

class TestTMListing():
    """
    Test to get/list all TMs by emails

    """
    @pytest.mark.django_db
    def test_listall_tms_successfully(self, client, new_tm,get_or_create_admin_token):
        token = get_or_create_admin_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        new_tm.save()
        url = reverse('staff:tm_listing')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        