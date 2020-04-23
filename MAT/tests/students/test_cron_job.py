from MAT.apps.students.cron_jobs import attendance_records_cronjob_creator


import datetime as dt
from datetime import datetime, timedelta

import pytest
from rest_framework import status

from MAT.apps.authentication.models import User
from MAT.apps.students.models import AttendanceRecords


class TestAttendanceEndpoints:
    @pytest.mark.django_db
    def test_student_can_check_in_successfully(self, get_or_create_token,new_user3):
        """Test for student check in"""
        created_records = []
        new_user3.save()

        token = get_or_create_token
        attendance_records_cronjob_creator()

        records = AttendanceRecords.objects.all()        
        assert  len(records)== 2
