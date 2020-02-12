from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from MAT.apps.authentication.models import User
from MAT.apps.common.base import CommonFieldsMixin
from MAT.apps.students.models import Students
from django.dispatch import receiver

class UserProfile(CommonFieldsMixin):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, default='Male')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profiles')
    student_class = models.CharField(
        max_length=255, default='MC21')
    fullname = models.CharField(
        max_length=255, default='firstname lastname')
    image = models.URLField(
        blank=True, null=True, default='https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiro')

    def __str__(self):
        return '{}'.format(self.user.username)

@receiver(post_save, sender=User)
@receiver(post_save, sender=Students)
def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = UserProfile.objects.create(user=instance)

