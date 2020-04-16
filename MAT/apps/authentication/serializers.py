from rest_framework import serializers
from .models import User; 


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        exclude = ('id', 'password', 
                    'last_login', 'created_at', 
                    'is_superuser', 'deleted', 
                    'user_permissions', 'updated_at', 
                    'groups', 'is_active')