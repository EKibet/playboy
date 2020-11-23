from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CohortListing, CohortViewSet,TMCohortsList,AdminAssignCohort,StudentAttendanceRecordsList

app_name = 'cohorts'

router = SimpleRouter()
router.register('cohorts', CohortViewSet, basename='cohorts')

urlpatterns = [
    path('cohorts/list/', CohortListing.as_view(), name='list'),
    path('tm-cohorts/list', TMCohortsList.as_view(), name='tm-list'),
    path('assign-cohort', AdminAssignCohort.as_view(),name='assign-cohort'),
    path('student-attendace-records/<student_id>/', StudentAttendanceRecordsList.as_view(),
        name='student-attendace-records')
] + router.urls
