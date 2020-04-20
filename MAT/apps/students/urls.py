from django.urls import include, path

from . import comments_views, views
from .views import ResetPasswordView, SendPasswordResetEmail

app_name = 'students'

urlpatterns = [
    path('students/upload', views.StudentInfoUploadView.as_view(),
         name='create_students'),
    path('students', views.StudentListAPIView.as_view(), name="list_students"),
    path('students/<str:email>', views.StudentDetailView.as_view(),
         name='student_details'),
    path('students/password/reset',
         views.SendPasswordResetEmail.as_view(), name='SendPasswordResetEmail'),
    path('students/password/reset/<token>',
         views.ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('students/check-in/', views.AttendanceRecordsAPIView.as_view(),
         name='attendance_checkin'),
    path('students/check-out/', views.AttendanceCheckoutApiView.as_view(),
         name='attendance_checkout'),
    path('students/verify/<str:token>', views.StudentVerificationAPIVIew.as_view(),
         name='student_verification'),
    path('comments/<int:record_id>', comments_views.CommentListAPIView.as_view(),
         name='list_attendance_records_comments'),
    path('create_comments/', comments_views.CommentsCreatePIView.as_view(),
         name='create_attendance_records_comments'),
    path('comment/<int:id>', comments_views.CommentRetrieveUpdateDestroy.as_view(),
         name='retrieve_attendance_records_comment'),
    path('students/attendance-records/', views.RetrieveAttendanceRecordsView.as_view(),
         name='attendance_records'),
]
