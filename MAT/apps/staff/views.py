from django.shortcuts import render
from .models import Staff
from django.contrib.auth.models import User
from .serializer import StaffListSerializer
from rest_framework import generics
# from rest_framework.permissions import IsAdminUser

class StaffListing(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
    # permission_classes = [IsAdminUser]