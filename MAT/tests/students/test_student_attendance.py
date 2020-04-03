import pytest
from django.urls import reverse
from rest_framework import status

from MAT.apps.authentication.models import User

from MAT.apps.students.models import AttendanceRecords
from django.utils import timezone

class TestAttendanceEndpoints:
    @pytest.mark.django_db
    def test_student_can_check_in_successfully(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        AttendanceRecords.objects.create(user_id=User.objects.get(email="sly@gmail.com"))

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data'][0]['fields']['is_present'] == True

    @pytest.mark.django_db
    def test_student_can_check_in_on_time_successfully(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        AttendanceRecords.objects.create(user_id=User.objects.get(email="sly@gmail.com"))

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data'][0]['fields']['is_present'] == True

    def test_check_in_cannot_work_for_nonexistent_attendancerecord(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'



    @pytest.mark.django_db
    def test_student_can_check_out_successfully(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        current_user=User.objects.get(email="sly@gmail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(user_id=current_user).update(checked_in=timezone.now())
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_student_can_check_out_on_time_successfully(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        current_user=User.objects.get(email="sly@gmail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(user_id=current_user).update(checked_in=timezone.now())
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')

        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK


    def test_check_out_cannot_work_for_nonexistent_attendancerecord(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'
    def test_cannot_checkout_if_you_did_not_checkin(self,client,get_or_create_token,create_attendance_record):
        """Test for student check in"""
        
        token=get_or_create_token
        create_attendance_record
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkout if you did not checkin'

    def test_cannot_student_account_not_verified(self,client,get_or_create_token,create_attendance_record):
        """Test for student check in"""
        
        token=get_or_create_token
        create_attendance_record
        User.objects.filter(email="sly@gmail.com").update(is_student=False)       
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Student account not verified!'


    def test_cannot_checkout_more_than_once(self,client,get_or_create_token,create_attendance_record):
        """Test for student check in"""
        
        token=get_or_create_token
        current_user=User.objects.get(email="sly@gmail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(user_id=current_user).update(is_checked_in=True,is_checked_out=True)
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkout more than once!'

    def test_cannot_find_attendace_record_matching_your_profile(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'


    def test_cannot_find_attendace_record_smatching_your_profile(self,client,get_or_create_token,change_time):
        """Test for student check in"""
        
        token=get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'


    def test_check_out_cannot_work_for_nonexistent_attendancerecord(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'

    def test_cannot_checkin_student_account_not_verified(self,client,get_or_create_token,create_attendance_record):
        """Test for student check in"""
        
        token=get_or_create_token
        create_attendance_record
        User.objects.filter(email="sly@gmail.com").update(is_student=False)       
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Student account not verified!'


    def test_cannot_checkin_more_than_once(self,client,get_or_create_token,create_attendance_record):
        """Test for student check in"""
        
        token=get_or_create_token
        current_user=User.objects.get(email="sly@gmail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(user_id=current_user).update(is_checked_in=True)
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkin more than once!'

    def test_cannot_checkin_find_attendace_record_matching_your_profile(self,client,get_or_create_token):
        """Test for student check in"""
        
        token=get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'


    def test_cannot_checkin_find_attendace_record_smatching_your_profile(self,client,get_or_create_token,change_time):
        """Test for student check in"""
        
        token=get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'
