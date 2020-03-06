from rest_framework import serializers

from MAT.apps.cohorts.models import Cohort


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('name', 'id', 'created_at', 'updated_at')

        read_only_fields = ('created_at', 'updated_at', 'id',)
