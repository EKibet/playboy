from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from MAT.apps.authentication.models import User
from MAT.apps.common.base import CommonFieldsMixin
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
        max_length=255, null=True,blank=True)
    fullname = models.CharField(
        max_length=255, default='firstname lastname')
    image = models.URLField(
        blank=True, null=True, default='https://res.cloudinary.com/mat-api/image/upload/v1589887195/profilepic_ilcie7.png')

    def __str__(self):
        return '{}'.format(self.user.username)

    def save_cohort(self):
        self.save()
@receiver(post_save, sender=User)
def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = UserProfile.objects.create(user=instance)
        if instance.is_student:
            UserProfile.objects.update_or_create(id=instance.user_profile.id, defaults={
                "fullname": instance.get_full_name
            })


