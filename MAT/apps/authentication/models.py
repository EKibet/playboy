from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


from MAT.apps.authentication.utility import student_cohort_assignment
from MAT.apps.cohorts.models import Cohort
from MAT.apps.common.base import CommonFieldsMixin


class User(AbstractUser, CommonFieldsMixin):
    """ Base class for all users"""
    is_verified = models.BooleanField(default=False,)
    # this is to track the changes on the model.
    history = HistoricalRecords()

    class Types(models.TextChoices):
        """User types"""
        TM = "TM", "Tm"
        STUDENT = "STUDENT", "Student"
        POD_LEADER = "POD_LEADER", "PodLeader"
        ADMIN = "ADMIN", "Admin"

    base_type = Types.ADMIN

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )
    email = models.CharField(_("email of User"), unique=True, max_length=255)
    cohort = models.ManyToManyField(Cohort, related_name='members', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
    
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

""" ===================================== Proxy Model Managers ================= """
class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)

class TmManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.TM)

class PodLeaderManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.POD_LEADER)



""" ============================== Proxy Models =================================== """

class Student(User):
    """class to create student objects & associated attributes"""
    base_type = User.Types.STUDENT
    objects = StudentManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True

class Tm(User):
    """ Class to create technical mentor objects & associated attributes"""
    base_type = User.Types.TM
    objects = TmManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TM
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True

class PodLeader(User):
    """Class to create pod leader objects & associated attributes"""
    base_type = User.Types.POD_LEADER
    objects = PodLeaderManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.POD_LEADER
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True


