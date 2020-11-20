from rest_framework import serializers
from django.core.exceptions import ValidationError
from MAT.apps.cohorts.models import Cohort
from datetime import datetime as dt


class CohortSerializer(serializers.ModelSerializer):
    cohort_name = serializers.CharField()
    class Meta:
        model = Cohort
        fields = ('cohort_name', 'id', 'created_at', 'updated_at','start_date','end_date')

        read_only_fields = ('created_at', 'updated_at', 'id',)
    
    def validate_end_date(self, value):
        '''This function validates the end date against the start date to only allow end dates to be ahead of the start date'''
        data = self.get_initial()
        start_date = dt.strptime(data.get('start_date'),'%Y-%m-%d').date()
        end_date = value

        if end_date <= start_date :
            raise ValidationError('The end date cannot be same or before the start date.')

        return end_date

