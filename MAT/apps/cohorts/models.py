from datetime import date as d, timedelta as td

from django.db import models
from simple_history.models import HistoricalRecords

from MAT.apps.common.base import CommonFieldsMixin


class Cohort(CommonFieldsMixin):
    """
    This is the cohort model for both the students and tms.
    """
    name = models.CharField(max_length=25, unique=True)
    start_date = models.DateField(default=d.today, blank=True, null=True)
    end_date = models.DateField(default=(d.today() + td(weeks=15)), blank=True, null=True)
    # this is to track the changes on the model.
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    

 

