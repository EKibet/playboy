import json
from datetime import datetime
from django.utils import timezone
from collections import OrderedDict

from django.core import serializers
from django.http import Http404
from django.shortcuts import get_list_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import User
from MAT.apps.common.pagination import CustomPagination
from MAT.apps.students.models import AttendanceComment, AttendanceRecords
from MAT.apps.students.serializers import (AttendanceCommentSerializer,
                                           AttendanceRecordsSerializer)
from MAT.apps.students.utility_functions import convert_date
from MAT.config.settings.base import env


class AttendanceRecordsAPIView(APIView):
    """
        Allows students checked-in
        Args:
            Valid Token

    """
    serializer_class = AttendanceRecordsSerializer
    def put(self, request):

        punctual_time_string = env.str('PUNCTUAL_TIME','05:30')
        strf_now=datetime.strftime(datetime.utcnow(),"%H:%M:%S")
        response = {
            "update": '',
            "error": ''
        }
        try:
            if strf_now <= punctual_time_string:
                attendance_record=get_list_or_404(AttendanceRecords,is_checked_in=False,user_id=request.user,user_id__is_student=True, date=datetime.today())[0]
                attendance_record.is_present=True
                attendance_record.checked_in=timezone.now()
                attendance_record.is_checked_in=True
                attendance_record.is_late=False
                attendance_record.attendance_number = attendance_record.attendance_number + 1
                attendance_record.save()
                res=serializers.serialize('json',[attendance_record])
                response['data']=json.loads(res)
                response['update'] = 'Checked in as punctual'

            elif(strf_now > punctual_time_string):

                attendance_record=get_list_or_404(AttendanceRecords,user_id=request.user,is_checked_in=False,user_id__is_student=True, date=datetime.today())[0]
                attendance_record.is_present=True
                attendance_record.checked_in=timezone.now()
                attendance_record.is_late=True
                attendance_record.is_checked_in=True
                attendance_record.attendance_number = attendance_record.attendance_number + (2/3)
                attendance_record.save()
                res=serializers.serialize('json',[attendance_record])
                response['data']=json.loads(res)
                response['update'] = 'Checked in as late'

            return Response(response, status=status.HTTP_200_OK)

        except Http404:
            message={"error":[]}
            if AttendanceRecords.objects.filter(is_checked_in=True, date=datetime.today()):
                message.get("error").append("Cannot checkin more than once!")
            if AttendanceRecords.objects.filter(user_id__is_student=False, date=datetime.today()):
                message.get("error").append("Student account not verified!")
            if len(AttendanceRecords.objects.filter(user_id=request.user, date=datetime.today())) == 0:
                message.get("error").append("Cannot find attendace record matching your profile!")

            return Response(message, status=status.HTTP_404_NOT_FOUND)


class AttendanceCheckoutApiView(APIView):
    """
        Allows students who checked-in to check-out
        Args:
            Valid Token

    """
    def put(self,request):
        check_out = env.str('CHECKOUT_TIME','15:00:00')
        strf_now=datetime.strftime(datetime.utcnow(),"%H:%M:%S")

        response = {
            "status": '',
            "data":{},
        }
        try:
            if strf_now <= check_out:
                attendance_record=get_list_or_404(AttendanceRecords,is_checked_out=False,user_id=request.user,checked_in__isnull=False, user_id__is_student=True,date=datetime.today())[0]
                attendance_record.checked_out=timezone.now()
                attendance_record.is_checked_out=True
                attendance_record.save()
                res=serializers.serialize('json',[attendance_record])
                response['data']=json.loads(res)
                response['status'] = 'Checked out earlier'
            elif(strf_now > check_out):
                attendance_record=get_list_or_404(AttendanceRecords,is_checked_out=False,user_id=request.user,checked_in__isnull=False, user_id__is_student=True,date=datetime.today())[0]
                attendance_record.checked_out=timezone.now()
                attendance_record.is_checked_out=True
                attendance_record.save()
                res=serializers.serialize('json',[attendance_record])
                response['data']=json.loads(res)
                response['status'] = 'Checked out within allowed time'
            return Response(response, status=status.HTTP_200_OK)

        except Http404:
            message={"error":[]}
            if AttendanceRecords.objects.filter(is_checked_in=False,date=datetime.today(),user_id__is_student=True):
                message.get("error").append("Cannot checkout if you did not checkin")
            if AttendanceRecords.objects.filter(user_id__is_student=False):
                message.get("error").append("Student account not verified!")
            if AttendanceRecords.objects.filter(is_checked_out=True, date=datetime.today()):
                message.get("error").append("Cannot checkout more than once!")
            if len(AttendanceRecords.objects.filter(user_id=request.user,date=datetime.today()))==0:
                message.get("error").append("Cannot find attendace record matching your profile!")

            return Response(message, status=status.HTTP_404_NOT_FOUND)

class RetrieveAttendanceRecordsView(APIView, CustomPagination):
    """
    Retrieves attendance records and their corresponding comments.
    args:
        valid token
        user_id
        date range
    """
    serializer_class = AttendanceRecordsSerializer
    serializer= AttendanceCommentSerializer

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get(self,request):
        records=[]
        start_date= convert_date(self.request.query_params.get("from_date"))
        to_date= convert_date(self.request.query_params.get("to_date"))
        attendance_records= AttendanceRecords.objects.filter(date__range=[to_date,start_date],user_id=self.request.query_params.get("user_id",request.user))
        for record in attendance_records:
            serializer = self.serializer_class(record)
            ready_data={}
            ready_data.update({record.date.strftime("%A"):serializer.data})
            serialized_comments=self.serializer(AttendanceComment.objects.filter(user_id=User.objects.get(id=self.request.query_params.get("user_id",request.user)),record=record),many=True,allow_empty=True)
            ready_data.get(record.date.strftime("%A")).update({"comments":serialized_comments.data})
            records.append(ready_data)
        paginated_records = self.paginate_queryset(records,request)
        return self.get_paginated_response(paginated_records)
