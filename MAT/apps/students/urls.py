from django.urls import include, path
from .views import SendPasswordResetEmail,ResetPasswordView
from . import views

app_name = 'students'

urlpatterns = [
    path('upload-student-info/', views.StudentInfoUploadView.as_view(),
         name='list_create_students'),
    path('create-cohort/', views.CohortCreateView.as_view(), name='cohort-creation'),
    path('list-students/', views.StudentListAPIView.as_view(), name="list_students"),
    path('students/SendPasswordResetEmail',
         SendPasswordResetEmail.as_view(), name='SendPasswordResetEmail'),
    path('students/ResetPasswordView/<token>',
         ResetPasswordView.as_view(), name='ResetPasswordView')
]
