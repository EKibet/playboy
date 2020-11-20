from rest_framework import generics, viewsets, mixins,status
from rest_framework.response import Response

from MAT.apps.cohorts.models import Cohort

from .renderers import CohortJSONRenderer, CohortsJSONRenderer
from .serializers import CohortSerializer
from rest_framework.views import APIView
from MAT.apps.authentication.models import User
from rest_framework.permissions import IsAdminUser
from MAT.apps.authentication.utility import student_cohort_assignment
from MAT.apps.common.permissions import IsPodLeaderOrAdmin


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
        