from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from simple_history.models import HistoricalRecords

from MAT.apps.common.base import CommonFieldsMixin
from MAT.apps.cohorts.models import Cohort
from django.db.models.signals import post_save
from MAT.apps.authentication.utility import student_cohort_assignment


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    
    def create_student(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, username and password."""
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        cohort_name = kwargs.get('cohort')
        if first_name is None:
            raise TypeError('Students must have a first name.')
        if kwargs.get('last_name') is None:
            raise TypeError('Students must have a last name.')

        if username is None:
            raise TypeError('Students must have a username.')

        if email is None:
            raise TypeError('Students must have an email address.')

        user = self.model(
            username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, cohort=student_cohort_assignment(cohort_name))
        user.set_password(password)
        user.is_student = True
        user.save()
        return user

    def create_staff(self, username, email, password=None, **kwargs):
        """Create and return a `User` with staff privileges eg a TM."""

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_staff(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(deleted=False)


class User(AbstractBaseUser, CommonFieldsMixin, PermissionsMixin):
    first_name = models.CharField(max_length=150, default='First')
    last_name = models.CharField(max_length=150, default='Last')
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=50, null=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True, null=False)

    # when a user is registered their account is not yet verified hence we
    # offer a way for the user to verify their account
    is_verified = models.BooleanField(default=False,)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False, )

    # The `is_student` flag is used to check if a student is logged in
    is_student = models.BooleanField(default=False,)

    # this is to track the changes on the model.
    history = HistoricalRecords()
    cohort = models.ForeignKey(
        Cohort, on_delete=models.CASCADE, related_name='members', null=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.first_name + self.last_name

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.first_name

    class Meta:
        ordering = ['-updated_at', '-created_at']


