from MAT.apps.authentication.models import User
from MAT.apps.students.models import AttendanceRecords


def attendance_records_cronjob_creator():
    queryset = User.objects.filter(is_student=True)
    for user in queryset:
        try:
            AttendanceRecords.objects.create(user_id=user)
        except:
            continue
