from celery import shared_task
from MAT.apps.common.utility import send_link

@shared_task
def celery_send_link(**kwargs):
    send_link(**kwargs)


@shared_task
def test_celery(**kwargs):
    print("The celery test works")
