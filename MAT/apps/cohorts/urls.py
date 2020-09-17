from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CohortListing, CohortViewSet,TMCohortsList

app_name = 'cohorts'

router = SimpleRouter()
router.register('cohorts', CohortViewSet, basename='cohorts')

urlpatterns = [
    path('cohorts/list/', CohortListing.as_view(), name='list'),
    path('tm-cohorts/list', TMCohortsList.as_view(), name='tm-list')
] + router.urls
