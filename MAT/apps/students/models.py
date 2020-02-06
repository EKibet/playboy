from django.db import models

from MAT.apps.authentication.models import User
from MAT.apps.common.base import CommonFieldsMixin

class Cohort(CommonFieldsMixin):
    name = models.CharField(max_length=255,db_index=True,unique=True)
    created_by = models.ForeignKey(User,related_name="cohort",null=True,on_delete=models.SET_NULL)
    

class Students(User):
    first_name = models.CharField(max_length=255,null=True)
    second_name = models.CharField(max_length=255,null=True)
    # uploaded_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL) #to-do
    student_cohort = models.ForeignKey(Cohort,related_name="students_cohort",null=True,on_delete=models.SET_NULL)
