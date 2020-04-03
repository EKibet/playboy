from rest_framework import serializers
from rest_framework.response import Response

from MAT.apps.authentication.models import User

from .models import AttendanceRecords


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'created_at', 'updated_at')

        read_only_fields = ('created_at', 'updated_at', 'username')


class AttendanceRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecords
        fields = ('is_present', 'is_late')
