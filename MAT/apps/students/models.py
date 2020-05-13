from django.db import models
import datetime

from MAT.apps.authentication.models import User
from MAT.apps.common.base import CommonFieldsMixin



class AttendanceRecords(CommonFieldsMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_present = models.BooleanField(default=False)
    is_late = models.BooleanField(default=True)
    checked_in = models.DateTimeField(null=True, blank=True)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    checked_out = models.DateTimeField(null=True, blank=True)
    date =  models.DateField(default=datetime.date.today)
    checked_in_time = models.TimeField(null=True)
    checked_out_time = models.TimeField(null=True)
    attendance_number=models.FloatField(default=0)


class AttendanceComment(CommonFieldsMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    record = models.ForeignKey(AttendanceRecords, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50, null=True)
    seen = models.BooleanField(default=False)
    check_out_comment = models.BooleanField(default=False)
    check_in_comment = models.BooleanField(default=False)
    date =  models.DateField(default=datetime.date.today)
