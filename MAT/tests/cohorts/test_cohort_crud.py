import json

import pytest
from django.urls import reverse
from rest_framework import status

from MAT.apps.authentication.models import User
from MAT.apps.cohorts.models import Cohort


class TestCohortCRUD():
    @pytest.mark.django_db
    def test_get_cohorts_list_succeeds(self, client, get_or_create_podleader_token):
        url = reverse('cohorts:list')
        token = get_or_create_podleader_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_cohort_save_succeeds(self, new_cohort):
        new_cohort.save()
        assert Cohort.objects.count() == 1

    @pytest.mark.django_db
    def test_cohort_name_succeeds(self, new_cohort):
        new_cohort.save()
        saved_cohort = Cohort.objects.latest('id')
        
        assert str(saved_cohort) == "MC01"

    @pytest.mark.django_db
    def test_create_cohort_succeeds(self, client, get_or_create_podleader_token):
        """Test creating a cohort """
        
        data = {
            "cohort_name": "MC31",
            "start_date": "2020-11-20"
        }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_read_cohort_succeeds(self, client, get_or_create_podleader_token, new_cohort):
        """Test getting an existing cohort """
       
        new_cohort.save()
        token = get_or_create_podleader_token
        latest_cohort = Cohort.objects.latest('id')
        url = reverse('cohorts:cohorts-detail', args=[str(latest_cohort.id)])

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_cohort_succeeds(self, client, get_or_create_podleader_token, new_cohort):
        """Test editing of an existing cohort """
        new_cohort.save()
        update_data = {
            "name": "MC134",
        }
        token = get_or_create_podleader_token
        latest_cohort = Cohort.objects.latest('id')
        url = reverse('cohorts:cohorts-detail', args=[str(latest_cohort.id)])

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.put(url, data=json.dumps(update_data),
                            content_type='application/json')
        latest_cohort = Cohort.objects.latest('id')
        assert response.status_code == status.HTTP_200_OK
        assert latest_cohort.name == "MC134"

    @pytest.mark.django_db
    def test_delete_cohort_succeeds(self, client, get_or_create_podleader_token, new_cohort):
        """Test deletion of an existing cohort """
        
        new_cohort.save()
        token = get_or_create_podleader_token
        latest_cohort = Cohort.objects.latest('id')
        url = reverse('cohorts:cohorts-detail', args=[str(latest_cohort.id)])

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.delete(url, content_type='application/json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_get_tm_cohorts_list_succeeds(self, client, get_or_create_podleader_token):
        url = reverse('cohorts:tm-list')
        token = get_or_create_podleader_token
        cohort1 = Cohort.objects.create(name="MC32")
        cohort2 = Cohort.objects.create(name="MC33")
        current_usr = User.objects.get(email='podleader@mail.com')
        current_usr.cohort.add(cohort1,cohort2)
        
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_get_student_att_records_by_id_successfully(self, client, get_or_create_token, create_attendance_record):
        create_attendance_record.save()
        current_user = User.objects.get(email="test@mail.com")
        student_id = str(current_user.id)
        url = reverse('cohorts:student-attendace-records', args=(student_id,))
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        response = client.get(url)
        assert len(response.data['results']) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_student_att_records_using_invalid_studentid(self, client, get_or_create_token):
        url = reverse('cohorts:student-attendace-records', args=(100,))
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_student_att_records_nonexistent_records(self, client, get_or_create_token, new_student):
        new_student.save()
        current_user = User.objects.get(email="test@mail.com")
        student_id = str(current_user.id)
        url = reverse('cohorts:student-attendace-records', args=(student_id,))
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    @pytest.mark.django_db
    def test_create_cohort_with_invalid_name_fails(self, client, get_or_create_podleader_token):
        """Test creating a cohort with invalid name """
        
        data = {
            "cohort_name": "MCZ31",
            "start_date": "2020-11-20"
        }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('name')[0] == "Invalid cohort name"

    @pytest.mark.django_db
    def test_create_cohort_with_existing_name_fails(self, client,new_cohort, get_or_create_podleader_token):
        """Test creating a cohort with existing name """
        new_cohort.save()
        data = {
            "cohort_name": "mc01",
            "start_date": "2020-11-20"
        }
        token = get_or_create_podleader_token
        url = reverse('cohorts:cohorts-list')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('name')[0] == "Cohort {} already exists".format(data.get('cohort_name').upper())