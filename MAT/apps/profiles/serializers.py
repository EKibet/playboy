from rest_framework import serializers, status
from rest_framework.response import Response

from MAT.apps.authentication.serializers import UserSerializer
from .models import StudentProfile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.URLField(required=True)
    profile_picture = serializers.ImageField(
        required=False, allow_empty_file=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'username')
