import csv
import os
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from MAT.apps.authentication.models import User
from MAT.apps.common.utility import send_link

from .serializers import StudentSerializer
from .renderers import (StudentJSONRenderer, StudentsJSONRenderer)


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
            'existing emails': existing_emails,
            'created emails': created_emails
        }
        try:
            for row in reader:
                try:
                    User.objects.create_student(username=row['Username'], email=row['email'],
                                                password='moringaschool', first_name=row['first_name'], last_name=row['second_name'],)
                    stats['created_count'] += 1
                    created_emails.append(row['email'])
                except IntegrityError:
                    existing_emails.append(row['email'])
                    stats['error_count'] += 1
            return Response(stats, status=status.HTTP_200_OK)
        except KeyError:
            message = {'error': 'CSV data does not have correct format.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
                               os.getenv('SECRET_KEY'), algorithm='HS256').decode('utf-8')
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
            decoded = jwt.decode(token, os.getenv(
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
