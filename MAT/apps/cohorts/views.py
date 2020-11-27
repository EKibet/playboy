import string

from rest_framework import generics, viewsets, mixins,status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.core.paginator import Paginator
from collections import OrderedDict


from MAT.apps.cohorts.models import Cohort

from MAT.apps.common.pagination import CustomPagination
from .renderers import CohortJSONRenderer, CohortsJSONRenderer
from .serializers import CohortSerializer
from MAT.apps.students.serializers import AttendanceRecordsSerializer
from rest_framework.views import APIView
from MAT.apps.authentication.models import User
from rest_framework.permissions import IsAdminUser
from MAT.apps.authentication.utility import student_cohort_assignment
from MAT.apps.common.permissions import IsPodLeaderOrAdmin
from MAT.apps.students.models import AttendanceComment, AttendanceRecords

class CohortListing(generics.ListAPIView):
    """A view to provide the listing functionality for the cohorts model

    Args:
        generics (Class): A generic class that will help in cohort listing.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    renderer_classes = (CohortsJSONRenderer,)


class CohortViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """A viewset that adds CRUD functionality for the cohorts model

    Args:
        viewsets (Class): A class that simplifies the creation of CRUD functionality
        in fewer lines of code.
    """
    permission_classes= [IsPodLeaderOrAdmin]
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    renderer_classes = (CohortJSONRenderer,)

    def create(self, request, **kwargs):
        cohort_data = {"name": request.data.get('cohort_name').upper(),
       "end_date": request.data.get('end_date'), "start_date": request.data.get('start_date')}

        serializer = self.serializer_class(
                data=cohort_data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                                status=status.HTTP_201_CREATED)



class TMCohortsList(APIView):
    serializer_class = CohortSerializer

    def get(self,request):
        cohorts = request.user.cohort.all()
        serializer = self.serializer_class(
            cohorts, many=True, allow_empty=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class AdminAssignCohort(generics.CreateAPIView):
    """
    Assign TMs a cohort using their emails

    * Only admin users are able to access this view.
    """
    permission_classes = [IsPodLeaderOrAdmin]
    def patch(self,request):
        tms = request.data['list_of_tms']
        cohort = student_cohort_assignment(request.data.get('cohort'))

        res={
            "cohort": "",
            "successful":[],
            "unsuccessful":[],
        }
        for email in tms:
            try:
                user=User.objects.get(email=email)
                user.cohort.add(cohort)
                res.get('successful').append(email)
                res["cohort"]=cohort.name
            except:
                res.get('unsuccessful').append(email)
        return Response(res, status=status.HTTP_200_OK)


class StudentAttendanceRecordsList(APIView, CustomPagination):
    """A view to provide the listing functionality for the attendance records of a specific
    student

    Args:
        APIView (Class): A class that will help in listing records.
    """
    serializer_class = AttendanceRecordsSerializer

    def get_paginated_response(self, data, user, att_summary):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('student', {
                "email": user.email,
                "id": user.id,
                "name": user.first_name + " " + user.last_name,
                "cohorts": user.current_cohorts
            }),
            ("summary", att_summary)
        ]))

    def get(self, request, student_id):
        user = User.objects.filter(pk=student_id)

        if not user or user[0].type != 'STUDENT':
            return Response({
                "message": "A student with that student_id does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        present_att_record = AttendanceRecords.objects.filter(user_id=student_id, is_present=True).count();
        att_records = AttendanceRecords.objects.filter(user_id=student_id)

        if att_records.count() == 0:
            return Response({
                "message": "The student has no existing attendance records"
            }, status=status.HTTP_404_NOT_FOUND)

        percentage_attendance = (present_att_record/att_records.count()) * 100;

        att_summary = {
            "overall_percentage": percentage_attendance
        }

        serializer = self.serializer_class(att_records, many=True, allow_empty=True)
        paginated_data = self.paginate_queryset(serializer.data, request)
        response = self.get_paginated_response(paginated_data, user[0], att_summary)

        return response
