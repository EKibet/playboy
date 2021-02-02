from rest_framework import serializers, status
from rest_framework.response import Response

from MAT.apps.authentication.serializers import UserSerializer
from .models import StudentProfile


class ProfileSerializer(serializers.ModelSerializer):
    TRACK_CHOICES = (
        ('prep', 'Prep'),
        ('angular', 'Angular'),
        ('flask', 'Flask'),
        ('java', 'Java'),
        ('django', 'Django'),
        ('android', 'Android'),
        ('dsprep', 'DSPrep'),
        ('dscore', 'DSCore'),
    )

    username = serializers.CharField(source='user.username', read_only=True)
    current_track = serializers.ChoiceField(choices=TRACK_CHOICES)
    image = serializers.URLField(required=True)
    profile_picture = serializers.ImageField(
        required=False, allow_empty_file=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'username')
