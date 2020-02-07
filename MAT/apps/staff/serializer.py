from rest_framework import serializers
from .models import Staff

class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id','username','first_name','last_name','gender','role','profile_pic','phone_number','email','is_active','is_verified','is_staff','is_student',)
        # fields = '__all__'
