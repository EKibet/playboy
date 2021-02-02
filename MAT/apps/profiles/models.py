from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from MAT.apps.authentication.models import Student
from MAT.apps.common.base import CommonFieldsMixin
from django.dispatch import receiver

class StudentCurrentTrack(CommonFieldsMixin):
    TRACK_CHOICES = (
        ('prep', 'Prep'),
        ('angular', 'Angular'),
        ('flask', 'Flask'),
        ('java', 'Java'),
        ('django', 'Django'),
        ('android', 'Android'),
        ('dsprep', 'DSPrep'),
        ('dscore', 'DSCore'),

    )
    track = models.CharField(
         max_length=30, choices=TRACK_CHOICES, default='prep')

    def __str__(self):
        return str(self.track)  


class StudentProfile(CommonFieldsMixin):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    image = models.URLField(
        blank=True, null=True, default='https://res.cloudinary.com/mat-api/image/upload/v1589887195/profilepic_ilcie7.png')
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, default='Male')
    student_class = models.CharField(
        max_length=255, null=True, blank=True)
    fullname = models.CharField(
        max_length=255, default='firstname lastname')      

    current_track = models.ForeignKey(
        StudentCurrentTrack, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "student_profile"

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=Student)
def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = StudentProfile.objects.create(user=instance)
        full_name = instance.first_name + ' '+  instance.last_name
        if instance:
            StudentProfile.objects.update_or_create(
                id=instance.user_profile.id,
                defaults={
                    "fullname":full_name
                })