import enum
from rest_framework import serializers
from .models import User

class SocialAuthSerializer(serializers.Serializer):

    token = serializers.CharField(required=True, allow_blank=False)
