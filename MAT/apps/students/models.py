from django.db import models
import datetime

from MAT.apps.authentication.models import User
from MAT.apps.common.base import CommonFieldsMixin


class AttendanceRecords(CommonFieldsMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_present = models.BooleanField(default=False)
    is_late = models.BooleanField(default=True)
    checked_in = models.DateTimeField(null=True)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    checked_out = models.DateTimeField(null=True)
    date =  models.DateField(default=datetime.date.today)



class AttendanceComment(CommonFieldsMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    record = models.ForeignKey(AttendanceRecords, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
