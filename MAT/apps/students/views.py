import csv

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from MAT.apps.common.utility import send_link

from MAT.apps.authentication.models import User
from datetime import datetime,timedelta
from .models import Cohort, Students


from .serializers import CohortSerializer, StudentListSerializer,StudentSerializer

from django.core.mail import send_mail
from django.conf import settings
import jwt
import os


class StudentInfoUploadView(APIView):
    parser_classes = (FileUploadParser,)
    serializer = StudentSerializer

    def post(self, request, format=None):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = list(csv.DictReader(decoded_file))
        stats = {
            'created_count': 0,
            'existed_count': 0,
            'error_count': 0,
            'error': [],
        }
        for row in reader:
            try:
                Students.objects.create(username=row['Username'], email=row['email'],
                                        password='moringaschool', first_name=row['first_name'], second_name=row['second_name'])
                stats['created_count'] += 1
            except:
                stats['error_count'] += 1
                stats['existed_count'] += 1
                stats['error'].append({"row": row, "errors": [{"message": "Username exists", "column": "username"}, {
                                      "message": "Email Exists", "column": "email"}]})
        return Response(stats)

    def get(self, request, format=None):
        students_queryset = Students.objects.all()
        serializer = StudentSerializer(students_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CohortCreateView(APIView):
    """
    List all cohorts, or create a new cohort.
    """

    def get(self, request, format=None):
        cohort_queryset = Cohort.objects.all()
        serializer = CohortSerializer(cohort_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CohortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentListAPIView(generics.ListAPIView):
    """
    An api view for returning the students list using the serializer
    """
    queryset = Students.objects.all()
    serializer_class = StudentListSerializer


class SendPasswordResetEmail(generics.CreateAPIView):
    def post(self, request):

        try:
            email = request.data.get('email')

            user_email = User.objects.get(email=email)

            subject = 'Password Reset'
            message = 'Your password reset request has been received '

            recipient = [user_email.email]
            payload = {'email': user_email.email,
                       "iat": datetime.now(),
                       "exp": datetime.utcnow()
                       + timedelta(minutes=20)

                       }
            token = jwt.encode(payload,
                               os.getenv('SECRET_KEY'), algorithm='HS256').decode('utf-8')
            url = 'api/students/students/reset/<token>'

            template = 'password_reset.html'
            send_link(user_email.email, subject, template, url, token)
            message = {
                "message": "Your email has been successfully sent",
                "token": token
            }
            return Response(message, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            message = {
                "message": "This email does not exist"
            }

        return Response(message, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(generics.CreateAPIView):

    def put(self, request, token):
        try:
            decoded = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(email=decoded['email'])
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
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            message = {
                'message': 'Email does not exist'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
