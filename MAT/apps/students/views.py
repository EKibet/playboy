import csv

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import User

from .models import Cohort, Students
from .serializers import (CohortSerializer, StudentListSerializer,
                          StudentSerializer)


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
