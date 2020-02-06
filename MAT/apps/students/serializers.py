from rest_framework import serializers
from rest_framework.response import Response

from MAT.apps.authentication.models import User

from .models import Cohort, Students


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ['name', 'created_by']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
