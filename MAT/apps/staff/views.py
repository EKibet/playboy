import csv
import os
from datetime import datetime, timedelta

import jwt
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import Student, User, Tm
from MAT.apps.common.utility import send_link

from .renderers import StaffJSONRenderer, TmJSONRenderer
from .serializer import StaffListSerializer, TMSerializer
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
                Student.objects.get(email=recipient)
                valid_emails.append(recipient)
            except Student.DoesNotExist:
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
            "invalid_emails": invalid_emails
        }
        return Response(message, status=status.HTTP_200_OK)


class StaffListing(generics.ListAPIView):
    """
    Returns the list of staff using the serializer.
    """
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffListSerializer
    renderer_classes = (StaffJSONRenderer,)


class SingleStaffListing(APIView):
    """
    API view that allows read,delete , update(patch) operations on a 
    single instance.
    Args:
        id: The staff user's id

    """
    renderer_classes = (StaffJSONRenderer,)

    def get(self, request, *args, **kwargs):
        staff = get_object_or_404(User, is_staff=True, pk=kwargs['id'])

        serializer = StaffListSerializer(staff)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        staff = get_object_or_404(User, is_staff=True, pk=kwargs['id'])
        serializer = StaffListSerializer(
            staff, data=request.data,  partial=True)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(StaffListSerializer(staff).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        staff = get_object_or_404(User, is_staff=True, pk=kwargs['id'])
        staff.delete()
        return Response("staff deleted", status=status.HTTP_204_NO_CONTENT)


class TmDetails(APIView):
    """
    API view that allows read,delete , update(patch) operations on a 
    single Tm instance.
    Args:
        id: The staff user's id

    """
    renderer_classes = (TmJSONRenderer,)

    def get(self, request, *args, **kwargs):
        staff = get_object_or_404(Tm, pk=kwargs['id'])

        serializer = TMSerializer(staff)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        staff = get_object_or_404(Tm, pk=kwargs['id'])
        serializer = TMSerializer(
            staff, data=request.data,  partial=True)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(TMSerializer(staff).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        staff = get_object_or_404(Tm, pk=kwargs['id'])
        staff.delete()
        return Response("TM deleted", status=status.HTTP_204_NO_CONTENT)


