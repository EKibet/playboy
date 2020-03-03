from django.urls import include, path
from .views import SendPasswordResetEmail,ResetPasswordView
from . import views

app_name = 'students'

urlpatterns = [
    path('students/upload', views.StudentInfoUploadView.as_view(),
         name='create_students'),
    path('students', views.StudentListAPIView.as_view(), name="list_students"),
    path('students/<str:email>', views.StudentDetailView.as_view(), name='student_details'),
    path('students/password/reset',
         SendPasswordResetEmail.as_view(), name='SendPasswordResetEmail'),
    path('students/password/reset/<token>',
         ResetPasswordView.as_view(), name='ResetPasswordView')
]
