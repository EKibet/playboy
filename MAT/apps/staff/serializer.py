from rest_framework import serializers

from MAT.apps.authentication.models import User


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'created_at', 'updated_at')

        read_only_fields = ('created_at', 'updated_at', 'username')
