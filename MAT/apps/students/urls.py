from django.urls import include, path

from . import views
app_name = 'students'

urlpatterns = [
    path('upload-student-info/', views.StudentInfoUploadView.as_view(),
         name='list_create_students'),
    path('create-cohort/', views.CohortCreateView.as_view(), name='cohort-creation')
]
