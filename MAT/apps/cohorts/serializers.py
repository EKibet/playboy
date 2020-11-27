import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MAT.apps.cohorts.models import Cohort

def validate_name(value):
    name = ''.join([character for character in value.upper() if value and character.isalnum()])
    if not re.match('MC[0-9]+', name):
        raise ValidationError('Invalid cohort name')
    if Cohort.objects.filter(name=name).exists():
        message = "Cohort {} already exists".format(name)
        raise ValidationError(message)

    return name

class CohortSerializer(serializers.ModelSerializer):

    name = serializers.CharField(validators=[validate_name])
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Cohort
        fields = ('name', 'id', 'created_at', 'updated_at','start_date','end_date')

        read_only_fields = ('created_at', 'updated_at', 'id',)
    
    def validate_end_date(self, value):
        '''This function validates the end date against the start date to only allow end dates to be ahead of the start date'''
        data = self.get_initial()
        if value:
            start = data.get('start_date')
            if not start:
                raise ValidationError("Please provide a start date")
            start_date = dt.strptime(start,'%Y-%m-%d').date()
            end_date = value

            if end_date <= start_date :
                raise ValidationError('The end date cannot be same or before the start date.')

            return end_date



