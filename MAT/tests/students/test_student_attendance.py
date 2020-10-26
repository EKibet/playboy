import datetime as dt
from datetime import datetime, timedelta
from urllib.parse import urlencode, urlparse

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from MAT.apps.authentication.models import Student, User
from MAT.apps.students.models import AttendanceRecords


class TestAttendanceEndpoints:
    @pytest.mark.django_db
    def test_student_can_check_in_successfully(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        AttendanceRecords.objects.create(
            user_id=Student.objects.get(email="test@mail.com"))

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data'][0]['fields']['is_present'] == True
        assert response.data['data'][0]['fields']['attendance_number'] == 0.6666666666666666
        assert response.data['update'] == 'Checked in as late'

    @pytest.mark.django_db
    def test_student_can_check_in_on_time_successfully(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        AttendanceRecords.objects.create(
            user_id=User.objects.get(email="test@mail.com"))

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data'][0]['fields']['is_present'] == True

    def test_check_in_cannot_work_for_nonexistent_attendancerecord(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'

    @pytest.mark.django_db
    def test_student_can_check_out_successfully(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        current_user = User.objects.get(email="test@mail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(
            user_id=current_user).update(checked_in=timezone.now())
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_student_can_check_out_on_time_successfully(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        current_user = User.objects.get(email="test@mail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(
            user_id=current_user).update(checked_in=timezone.now())
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')

        response = client.put(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_check_out_cannot_work_for_nonexistent_attendancerecord(self, client, get_or_create_admin_token):
        """Test for student check in"""

        token = get_or_create_admin_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'

    @pytest.mark.django_db
    def test_cannot_checkout_if_you_did_not_checkin(self, client, get_or_create_token, create_attendance_record):
        """Test for student check in"""

        token = get_or_create_token
        create_attendance_record.save()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkout if you did not checkin'

    @pytest.mark.django_db
    def test_cannot_checkout_more_than_once(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        current_user = Student.objects.get(email="test@mail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(user_id=current_user).update(
            is_checked_in=True, is_checked_out=True)
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkout more than once!'

    @pytest.mark.django_db
    def test_cannot_find_attendace_record_matching_your_profile(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'

    def test_cannot_find_attendace_record_smatching_your_profile(self, client, get_or_create_token, change_time):
        """Test for student check in"""

        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkout')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot find attendace record matching your profile!'

    def test_cannot_checkin_more_than_once(self, client, get_or_create_token, create_attendance_record):
        """Test for student check in"""

        token = get_or_create_token
        current_user = User.objects.get(email="test@mail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        AttendanceRecords.objects.filter(
            user_id=current_user).update(is_checked_in=True)
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        url = reverse('students:attendance_checkin')
        response = client.put(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'][0] == 'Cannot checkin more than once!'

    def test_cannot_checkin_find_attendace_record_matching_your_profile(self, client, get_or_create_token):
        """Test for student check in"""

        token = get_or_create_token
        url = reverse('students:attendance_checkin')
        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
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


class TestAttendanceRecordsRetrieve:
    @pytest.mark.django_db
    def test_can_retreive_records_between_specified_date_range(self, client, get_or_create_token, create_attendance_record):
        token = get_or_create_token

        client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        current_user = User.objects.get(email="test@mail.com")
        AttendanceRecords.objects.create(user_id=current_user)
        from_date = datetime.today().date().isoformat()
        to_date = (datetime.today()-timedelta(days=20)).date().isoformat()
        params={"user_id": current_user.id, "from_date": from_date, "to_date": to_date}
        params = urlencode(params)
        url = reverse('students:attendance_records')+"?"+params
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
