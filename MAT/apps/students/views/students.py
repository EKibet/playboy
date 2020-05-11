import csv

from django.db import IntegrityError
from rest_framework import status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import User
from MAT.apps.common.pagination import CustomPagination
from MAT.config.settings.base import env

from MAT.apps.students.serializers import StudentSerializer
from MAT.apps.students.renderers import (StudentJSONRenderer, StudentsJSONRenderer)


class StudentInfoUploadView(APIView):  # pragma: no cover
    """
    This view creates users(students) from CSV data
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


