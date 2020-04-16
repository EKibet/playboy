from django.contrib import admin
from .models import AttendanceRecords, AttendanceComment


admin.site.register(AttendanceComment)
admin.site.register(AttendanceRecords)