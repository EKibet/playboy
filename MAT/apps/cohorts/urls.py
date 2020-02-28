from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CohortListing, CohortViewSet

app_name = 'cohorts'

router = SimpleRouter()
router.register('cohorts', CohortViewSet, basename='cohorts')

urlpatterns = [
    path('cohorts/list/', CohortListing.as_view(), name='list')
] + router.urls
