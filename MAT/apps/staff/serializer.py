from rest_framework import serializers

from MAT.apps.authentication.models import User, Tm, PodLeader
from MAT.apps.cohorts.serializers import CohortSerializer


class StaffListSerializer(serializers.ModelSerializer):
    cohort = CohortSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'created_at', 'updated_at', "cohort", "cohort_history", "current_cohorts")

        read_only_fields = ('created_at', 'updated_at', 'username', 'email',)
        depth = 1


class TMSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tm
        fields = ('first_name', 'last_name', 'email',
                  'username', 'created_at', 'updated_at', "cohort_history", "current_cohorts")

        read_only_fields = ('created_at', 'updated_at', 'username', 'email',)
        depth = 1


class PodLeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodLeader
        fields = ('first_name', 'last_name', 'email',
                  'username', 'current_cohorts', 'deleted')

        read_only_fields = ('created_at', 'updated_at', 'username', 'email',)
        depth = 1

