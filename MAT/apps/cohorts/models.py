from django.db import models
from simple_history.models import HistoricalRecords

from MAT.apps.common.base import CommonFieldsMixin


class Cohort(CommonFieldsMixin):
    """
    This is the cohort model for both the students and tms.
    """
    name = models.CharField(max_length=25, unique=True)
    # this is to track the changes on the model.
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def cohort_name(self):
        return self.name

    @cohort_name.setter
    def cohort_name(self,value):
        self.name = ''.join([character for character in value.upper() if value and character.isalnum()])
    

 

