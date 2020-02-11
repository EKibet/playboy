from django.urls import include, path
from .views import SendPasswordResetEmail,ResetPasswordView
from . import views

app_name = 'students'

urlpatterns = [
    path('upload', views.StudentInfoUploadView.as_view(),
         name='create_students'),
    path('', views.StudentListAPIView.as_view(), name="list_students"),
    path('<str:email>', views.StudentDetailView.as_view(), name='student_details'),
    path('students/SendPasswordResetEmail',
         SendPasswordResetEmail.as_view(), name='SendPasswordResetEmail'),
    path('students/ResetPasswordView/<token>',
         ResetPasswordView.as_view(), name='ResetPasswordView')
]
