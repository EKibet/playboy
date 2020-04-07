import csv
import json
import os
from datetime import datetime, timedelta, date

import jwt
import pytz
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_list_or_404, render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import exceptions

from MAT.apps.authentication.models import User
from MAT.apps.common.utility import send_link
from MAT.config.settings.base import env

from .models import AttendanceRecords
from .serializers import StudentSerializer,StudentRegistrationSerializer, AttendanceRecordsSerializer
from .renderers import (StudentJSONRenderer, StudentsJSONRenderer)
from django.contrib.sites.shortcuts import get_current_site


class StudentInfoUploadView(APIView):  # pragma: no cover
    """
    This view creates users(stdents) from CSV data
        Args: CSV data
        Returns: Student emails that have been successfully created

    """
    parser_classes = (FileUploadParser,)
    serializer = StudentSerializer
    renderer_classes = (StudentsJSONRenderer,)

    def post(self, request, format=None):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = list(csv.DictReader(decoded_file))
        existing_emails = []
        created_emails = []
        stats = {
            'created_count': 0,
            'error_count': 0,
            'existing_emails': existing_emails,
            'created_emails': created_emails,
        }
        # def send_link(email, subject, template, url, *args):
        try:
            for row in reader:
                try:
                    User.objects.create_student(username=row['Username'], email=row['email'],
                                                password=env.str('STUDENTS_PASSWORD','moringaschool'), first_name=row['first_name'], last_name=row['second_name'],)
                    stats['created_count'] += 1
                    created_emails.append(row['email'])
                except IntegrityError:
                    existing_emails.append(row['email'])
                    stats['error_count'] += 1
            return Response(stats, status=status.HTTP_200_OK)
        except KeyError:
            message = {'error': 'CSV data does not have correct format.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class StudentVerificationAPIVIew(generics.GenericAPIView):
    serializer_class = StudentSerializer
    # by this time the student will not be able to login,
    # therefore lets allow unauthenticated  requests for this endpoint.
    permission_classes = (AllowAny,)

    def get(self, request, token):
        """
        Given a token, we decode the token get the user and activate him/her
        """
        try:
            payload = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignature:
            msg = "Token has a expired, please generate a new one"
            raise exceptions.ValidationError(msg)

        # get the user then check if he is verified
        user = User.objects.get(pk=payload['user_id'])

        # first check if the user is verified
        if user.is_verified == False:
            user.is_verified = True
            user.save()
            return Response({"message": "account verified successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "You have already verified your account"}, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    serializer_class = StudentSerializer
    renderer_classes = (StudentJSONRenderer,)

    def get(self, request, email):
        try:
            user = User.objects.get(email=email, is_student=True)
        except:
            message = {"error": "User does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, email):
        try:
            user = User.objects.get(email=email, is_student=True)
        except:
            message = {"error": "User does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = self.serializer_class(
            instance=user, data=data, partial=True,
            context={
                'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentListAPIView(generics.ListAPIView):
    """
    An api view for returning the students list using the serializer
    """
    queryset = User.objects.filter(is_student=True)
    serializer_class = StudentSerializer
    renderer_classes = (StudentsJSONRenderer,)


class SendPasswordResetEmail(APIView):
    """
    Allows users to send password reset requests
    Args:
        email: The email ssociated with the account
    """
    permission_classes = (AllowAny,)

    def post(self, request):

        try:
            email = request.data.get('email')

            user_email = User.objects.get(email=email)

            subject = 'Password Reset'
            message = 'Your password reset request has been received '

            recipient = [user_email.email]
            payload = {'email': recipient,
                       "iat": datetime.now(),
                       "exp": datetime.utcnow()
                       + timedelta(minutes=20)
                       }
            token = jwt.encode(payload,
                               env.str('SECRET_KEY'), algorithm='HS256').decode('utf-8')
            url = '/students/password/reset/{}'.format(token)

            template = 'password_reset.html'
            send_link(user_email.email, subject, template, url, token)
            message = {
                "message": "email has been successfully sent",
                "token": token
            }
            return Response(message, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            message = {
                "message": "This email does not exist"
            }

        return Response(message, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    """
    Allows users to reset their account passwords
    Args:
        password: The new account password
        confirm_password: Has to match the new account password
    """
    permission_classes = (AllowAny,)

    def put(self, request, token):
        try:
            decoded = jwt.decode(token, env.str(
                'SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(email=decoded['email'][0])
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')

            if password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                message = {
                    "message": "Password has been confirmed"
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {
                    "message": "The passwords do not match"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:               # pragma: no cover
            message = {
                'message': 'User does not exist'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)

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
            if len(AttendanceRecords.objects.filter(user_id=request.user)) == 0:
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
                     

class SingleUserRegistrationView(generics.CreateAPIView):
    """
    Allows a staff to create single student's account
    Args:
        first_name: the student's first name
        last_name: the student's last name
        username: username that will be indexed by the system
        email: the student's email
        password: The new account password
    """
    permission_classes =[IsAdminUser]
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = request.data.get('email')
        message = {0:"User created Successfully", 1:"User already exists"}
        if User.objects.filter(email=user_email).exists():
            return Response(message[1], status=status.HTTP_400_BAD_REQUEST )
        serializer.save()
        return Response(message[0], status= status.HTTP_201_CREATED)
