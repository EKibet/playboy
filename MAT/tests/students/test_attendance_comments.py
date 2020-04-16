import pytest
import json
from rest_framework.utils.serializer_helpers import ReturnList


from django.urls import reverse
from rest_framework import status
from MAT.apps.students.models import AttendanceComment

class TestAttendanceCommentsList:

    @pytest.mark.django_db
    def test_get_attendance_commnets_list_ok(self, client, get_or_create_token, new_comment_list): 
        """ test get comments list """
        token = get_or_create_token
        new_comment_list.save()
        url = reverse('students:list_attendance_records_comments', kwargs={'record_id': 1})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_attendance_commnets_list_type(self, client, get_or_create_token, new_comment_list): 
        """ test get comments list type """
        token = get_or_create_token
        new_comment_list.save()
        url = reverse('students:list_attendance_records_comments', kwargs={'record_id': 1})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)        
        assert True == isinstance(response.data, ReturnList)

    @pytest.mark.django_db
    def test_get_attendance_commnets_list_empty_record(self, client, get_or_create_token, new_comment_list): 
        """ test get comments empty record"""
        token = get_or_create_token
        new_comment_list.save()
        url = reverse('students:list_attendance_records_comments', kwargs={'record_id': 2})
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)        
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_create_attendance_record_201(self, client, get_or_create_token, new_record):
        new_record.save()
        token = get_or_create_token
        url = reverse('students:create_attendance_records_comments')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)

        comment_data = {
           "relevant_date": "2020-02-28", 
	        "text": "I got caught up in traffic",
	        "tag": "absent"
            }
        token = get_or_create_token
        url = reverse('students:create_attendance_records_comments')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(comment_data),
                              content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_attendance_record_late_tag(self, client, get_or_create_token, new_record):
        new_record.save()
        token = get_or_create_token
        url = reverse('students:create_attendance_records_comments')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(url)

        comment_data = {
           "relevant_date": "2020-02-28", 
	        "text": "I got caught up in traffic",
	        "tag": "late"
            }
        token = get_or_create_token
        url = reverse('students:create_attendance_records_comments')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(url, data=json.dumps(comment_data),
                              content_type='application/json')
        assert 'late' in str(response.data)

