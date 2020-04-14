from django.db import IntegrityError
from rest_framework import serializers, status
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
class StudentRegistrationSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=100) 
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=4, max_length=100,write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password',
            'first_name', 'last_name',] 
        extra_kwargs = {
            'password': {'write_only': True}
            }
    
    def create(self, validated_data): 
        user = User.objects.create_student(
            **validated_data 
            )
        return user
