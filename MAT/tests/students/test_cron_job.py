from MAT.apps.students.cron_jobs import attendance_records_cronjob_creator


import datetime as dt
from datetime import datetime, timedelta

import pytest
from rest_framework import status

from MAT.apps.authentication.models import User
from MAT.apps.students.models import AttendanceRecords


class TestCronJob:
    @pytest.mark.django_db
    def test_attendance_cron_creates_records_successfully(self,new_user3):
        new_user3.save()
        attendance_records_cronjob_creator()

        records = AttendanceRecords.objects.all()        
        assert  len(records)== 1
