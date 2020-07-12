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
    cohort = models.ManyToManyField(
        Cohort, through='CohortMembership', related_name='members', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
    
        return super().save(*args, **kwargs)
    
    @property
    def cohort_history(self):
        cohort_history = []

        self_history = self.cohort.all()

        for cohort_instance in self_history:
            cohort = {}
            try:
                cohort["cohort_id"] = cohort_instance.id
                cohort["cohort_name"] = cohort_instance.name
            except Exception as e:
                continue
            cohort_history.append(cohort)
        return cohort_history

    @property
    def current_cohorts(self):
        current_cohorts_list = []

        membership_history = CohortMembership.objects.filter(
            user=self, current_cohort=True)

        for membership in membership_history:
            cohort = {}
            cohort_instance = membership.cohort
            try:
                cohort["cohort_id"] = cohort_instance.id
                cohort["cohort_name"] = cohort_instance.name
            except Exception as e:
                continue
            current_cohorts_list.append(cohort)
        return current_cohorts_list

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

class CohortMembership(models.Model):
    """A model used for representing membership of  tms in cohorts
    Add current_cohort field to track the current cohort for the user
    Args:
        models ([Model]): [Inherit from django Model]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    current_cohort = models.BooleanField(null=True)