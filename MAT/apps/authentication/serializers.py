import enum
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'password',
                    'last_login', 'created_at',
                    'is_superuser', 'deleted',
                    'user_permissions', 'updated_at',
                    'groups', 'is_active')


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Roles(enum.Enum):
        student = 'student'
        staff = 'staff'

    password = serializers.CharField(min_length=4, max_length=100,write_only=True)
    roles = [role.value for role in Roles]
    role = serializers.ChoiceField(choices=roles)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username','email', 'password','role']


        extra_kwargs = {
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        role = self.validated_data['role']
        if role == 'student':
            user = User.objects.create_student(
                **validated_data
                )

        else:
            user = User.objects.create_staff(
                **validated_data
                )
        return user
