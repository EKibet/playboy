import datetime as dt
from datetime import date, datetime, timedelta
from django.db.models import Sum

from MAT.apps.cohorts.models import Cohort
from MAT.apps.students.models import AttendanceRecords

def convert_date(raw_date):
    return dt.date(*(int(s) for s in raw_date.split('-')))

def calculate_student_attendance(user_id):
    queryset = AttendanceRecords.objects.filter(user_id=user_id)
    attendance = {
        "attendance_percentage": "",
        "punctual": "",
        "late": "",
        "absent": ""
    }
    error = {"no attendance records found"}
    if queryset.count() >= 1:
        total_attendance = queryset.aggregate(Sum('attendance_number'))
        total_records = queryset.count()
        total_absent_records = queryset.filter(attendance_number=0).count()
        attendance['absent'] = total_absent_records
        total_punctual_records = queryset.filter(attendance_number=1).count()
        attendance['punctual'] = total_punctual_records
        total_late_records = total_records - total_absent_records - total_punctual_records
        attendance['late'] = total_late_records
        attendance_percentage =  total_attendance['attendance_number__sum'] / total_records * 100
        attendance['attendance_percentage'] = attendance_percentage
        return attendance
    return error