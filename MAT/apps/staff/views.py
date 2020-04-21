import os
from datetime import datetime, timedelta

import jwt
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import User
from MAT.apps.common.utility import send_link

from .renderers import StaffJSONRenderer
from .serializer import StaffListSerializer
from .tasks import celery_send_link


class SendEmails(APIView):

    def post(self, request):
        subject = request.data.get('subject', None)
        message = request.data.get('message', None)
        recipients = request.data.get('recipients', None)
        valid_emails = []
        invalid_emails = []
        for recipient in recipients:
            try:
                User.objects.get(email=recipient)
                valid_emails.append(recipient)
            except User.DoesNotExist:
                invalid_emails.append(recipient)
                continue
        if len(invalid_emails) > 0:
            message = {
                "message": "These emails were not sent",
                "invalid_emails": invalid_emails
            }
        for email in valid_emails:
            payload = {'email':  email,
                       "iat": datetime.now(),
                       "exp": datetime.utcnow()
                       + timedelta(hours=48)}
            token = jwt.encode(payload,
                               os.getenv('SECRET_KEY'),
                               algorithm='HS256').decode('utf-8')
            url = '/students/verify/'
            template = 'student_invite_template.html'

            kwargs = {"email": email, "subject": subject,
                      "template": template, "url": url, "token": token}
            celery_send_link.delay(**kwargs)
        message = {
            "success": "{} emails were successfully sent.".format(len(valid_emails)),
            "fail": "{} emails failed.".format(len(invalid_emails)),
            "invalid_emails":invalid_emails
        }
        return Response(message, status=status.HTTP_200_OK)


class StaffListing(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffListSerializer
    renderer_classes = (StaffJSONRenderer,)
