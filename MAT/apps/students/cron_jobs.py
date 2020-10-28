from MAT.apps.authentication.models import Student
from MAT.apps.students.models import AttendanceRecords

# pragma: no cover
def attendance_records_cronjob_creator():
    queryset = Student.objects.filter(is_verified=True)
    for user in queryset:
        try:
            AttendanceRecords.objects.create(user_id=user)
        except:
            continue
