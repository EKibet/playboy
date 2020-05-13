import datetime as dt
from datetime import date, datetime, timedelta
from MAT.apps.cohorts.models import Cohort

def convert_date(raw_date):
    return dt.date(*(int(s) for s in raw_date.split('-')))

