import csv
import os
from datetime import datetime, timedelta

import jwt
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from MAT.apps.authentication.models import Student, User, Tm, PodLeader
from MAT.apps.common.utility import send_link

from .renderers import StaffJSONRenderer, TmJSONRenderer, PodLeaderRenderer
from .serializer import StaffListSerializer, TMSerializer, PodLeaderSerializer
from .tasks import celery_send_link

from MAT.apps.common.permissions import IsPodLeaderOrAdmin, IsAdminOrReadOnly
from .renderers import StaffJSONRenderer, TmJSONRenderer
from .serializer import StaffListSerializer, TMSerializer,TMListSerializer
from .tasks import celery_send_link
from rest_framework import viewsets
from MAT.apps.common.permissions import IsPodLeaderOrAdmin


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
                               algorithm='HS256')
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

        
    permission_classes = [IsPodLeaderOrAdmin]
    def delete(self, request, *args, **kwargs):
        staff = get_object_or_404(Tm, pk=kwargs['id'])
        staff.delete()
        return Response("TM deleted", status=status.HTTP_204_NO_CONTENT)

class TMListingViewSet(viewsets.ViewSet):
    """
    API endpoint for listing TMs by emails

    """
    queryset = Tm.objects.all()
    serializer_class = TMListSerializer

    def list(self,request):
        tms = Tm.objects.all()
        serializer = TMListSerializer(tms, many=True)
        return Response(serializer.data)







class PodLeaderDetails(APIView):
    ''' The Pod leaders detail view. 
        The functions herein will return a 404 if the object was soft deleted from the database. This implementation ensures that the queryset does not include deleted records.
        Anyone can view the records but only the admins have the CUD permissions
    '''

    permission_classes = (IsAdminOrReadOnly,)
    renderer_classes = (PodLeaderRenderer,)
    serializer_class = PodLeaderSerializer

    def get(self, request, *args, **kwargs):
        pod_leader = get_object_or_404(PodLeader, deleted=False,id=kwargs['id'])
        serializer = self.serializer_class(pod_leader)
       
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pod_leader = get_object_or_404(PodLeader, deleted= False, id=kwargs['id'])
        serializer = self.serializer_class(
            pod_leader, request.data, partial= True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pod_leader = get_object_or_404(PodLeader, deleted=False, id=kwargs['id'])
        pod_leader.delete()
        message = f'{pod_leader.username} deleted successfully!'

        return Response(message, status.HTTP_200_OK)