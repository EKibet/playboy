from rest_framework import serializers

from .models import UserProfile
from rest_framework.response import Response
from rest_framework import status


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.URLField(required=False)


    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'username')
