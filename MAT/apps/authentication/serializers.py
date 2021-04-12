import enum
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MAT.apps.authentication.utility import student_cohort_assignment

from .models import CohortMembership, PodLeader, Student, Tm, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 


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
        TM = "TM", "Tm"
        STUDENT = "STUDENT", "Student"
        POD_LEADER = "POD_LEADER", "PodLeader"

    password = serializers.CharField(min_length=4, max_length=100,write_only=True)
    roles = [role.value for role in Roles]
    role = serializers.ChoiceField(choices=roles, required=True)
    cohort = serializers.CharField(max_length=100, allow_blank=True, required=False)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username','email', 'password','role', 'cohort']


        extra_kwargs = {
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        role = self.validated_data['role']
        if role == 'STUDENT':
            user = Student.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                type=role
                )
            cohort_name = validated_data.get('cohort')
            cohort = student_cohort_assignment(cohort_name)
            # add student membership to the cohort
            membership = CohortMembership(
                user=user, cohort=cohort, current_cohort=True)
            membership.save()

        elif role == 'TM':
            user = Tm.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                type=role
                )
            cohort_name = validated_data.get('cohort')
            cohort = student_cohort_assignment(cohort_name)
            # add tm membership to the cohort
            membership = CohortMembership(
                user=user, cohort=cohort, current_cohort=True)
            membership.save()

        else:
            user = PodLeader.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                type=role
                )
            cohort_name = validated_data.get('cohort')
            cohort = student_cohort_assignment(cohort_name)
            # add pod-leader membership to the cohort
            membership = CohortMembership(
                user=user, cohort=cohort, current_cohort=True)
            membership.save()
        return user

class SignOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

class SocialAuthSerializer(serializers.Serializer):

    token = serializers.CharField(required=True, allow_blank=False)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['role']=user.type
        return token
