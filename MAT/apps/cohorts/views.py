from rest_framework import generics, viewsets, mixins,status
from rest_framework.response import Response

from MAT.apps.cohorts.models import Cohort

from .renderers import CohortJSONRenderer, CohortsJSONRenderer
from .serializers import CohortSerializer,TMCohortSerializer
from rest_framework.views import APIView
from MAT.apps.authentication.models import User


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
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    renderer_classes = (CohortJSONRenderer,)

class TMCohortsList(APIView):
    serializer_class = TMCohortSerializer

    def get(self,request):
        cohorts = request.user.cohort.all()
        serializer = self.serializer_class(
            cohorts, many=True, allow_empty=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
