from rest_framework import serializers

from MAT.apps.cohorts.models import Cohort


class CohortSerializer(serializers.ModelSerializer):
    cohort_name = serializers.CharField()
    class Meta:
        model = Cohort
        fields = ('cohort_name', 'id', 'created_at', 'updated_at')

        read_only_fields = ('created_at', 'updated_at', 'id',)
