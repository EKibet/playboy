from MAT.apps.authentication.models import User
from MAT.apps.students.models import AttendanceRecords

# pragma: no cover
def attendance_records_cronjob_creator():
    queryset = User.objects.filter(is_student=True, is_verified=True)
    for user in queryset:
        try:
            AttendanceRecords.objects.create(user_id=user)
        except:
            continue
