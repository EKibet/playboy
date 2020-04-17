import datetime as dt
from datetime import date, datetime, timedelta

def convert_date(raw_date):
    return dt.date(*(int(s) for s in raw_date.split('-')))