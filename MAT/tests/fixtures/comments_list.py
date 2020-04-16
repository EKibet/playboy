import pytest 
from django.urls import reverse
from MAT.apps.students.models import AttendanceComment, AttendanceRecords
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



    
@pytest.fixture(scope='function')
def new_record(new_user, django_db_blocker):
    with django_db_blocker.unblock():
        new_user.save()
        params = {
            "created_at": "2020-02-28 05:49:05.923982+03", 
            "updated_at": "2020-02-28 05:49:05.924029+03", 
            "is_present": True,
            "user_id_id": new_user.id
        }
    return AttendanceRecords(**params)


@pytest.fixture(scope='function')
def new_comment_list(django_db_blocker, new_user, new_record):
    new_user.save()
    new_record.save()
    with django_db_blocker.unblock():
        params = {
            "record": new_record,
            "text": "I am sorry I wont attend tommorows class ", 
            "tag": "absent",
            "user_id_id": new_user.id

        }
    return AttendanceComment(**params)
