from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from .cron_jobs import attendance_records_cronjob_creator

logger = get_task_logger(__name__)



@periodic_task(run_every=(crontab(hour=4, minute=30)), name="cronjob", ignore_result=True)
def create_students_records():
    logger.info("create students records")
    return attendance_records_cronjob_creator()
