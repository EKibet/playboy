from django.db import models
from MAT.apps.authentication.models import User


# Create your models here.
class Staff(User):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    role = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to = 'profile_pic/', null =True, blank = True)
    phone_number = models.IntegerField(blank =True, null = True)

