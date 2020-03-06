from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response

from MAT.apps.cohorts.models import Cohort

from .renderers import CohortJSONRenderer, CohortsJSONRenderer
from .serializers import CohortSerializer


class CohortListing(generics.ListAPIView):
    """A view to provide the listing functionality for the cohorts model

    Args:
        generics (Class): A generic class that will help in cohort listing.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = (permissions.AllowAny,)
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
    permission_classes = (permissions.AllowAny,)
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    renderer_classes = (CohortJSONRenderer,)
