from django.shortcuts import render
from .models import Staff
from django.contrib.auth.models import User
from .serializer import StaffListSerializer
from rest_framework import generics, status
# from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from rest_framework.response import Response
from MAT.apps.authentication.models import User
from MAT.apps.common.utility import send_link
from datetime import datetime, timedelta
import jwt
import os

class SendEmails(generics.CreateAPIView):

    def post(self, request):
        subject = request.data.get('subject', None)
        message = request.data.get('message', None)
        sender = request.data.get('sender', None)
        recipients = request.data.get('recipients', None)
        valid_emails = [recipient for recipient in recipients if User.objects.filter(email=recipient)]
        if len(valid_emails) < 1:
            message = {
                "message": "There were no emails sent. Confirm that the right emails were input."
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        for email in valid_emails:
            payload = {'email':  email,
                        "iat": datetime.now(),
                        "exp": datetime.utcnow()
                        + timedelta(hours=72)}
            token = jwt.encode(payload,
                    os.getenv('SECRET_KEY'),
                    algorithm='HS256').decode('utf-8')
            url = '/api/students/verify/'
            template = 'student_invite_template.html'
            send_link(email,subject, template, url, token)
        message = {
            "message": "Your emails were successfully sent."
        }
        return Response(message, status=status.HTTP_200_OK)

class StaffListing(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
    # permission_classes = [IsAdminUser]
