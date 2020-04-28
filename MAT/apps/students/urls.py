from django.urls import path

from MAT.apps.students.views import students, attendance, comments_views
from MAT.apps.students.views.attendance import SingleUserRegistrationView
from MAT.apps.students.views.password_reset import SendPasswordResetEmail, \
    ResetPasswordView
from MAT.apps.students.views.verification import StudentVerificationAPIVIew

app_name = 'students'

urlpatterns = [
    path('students/upload', students.StudentInfoUploadView.as_view(),
         name='create_students'),
    path('students', students.StudentListAPIView.as_view(), name="list_students"),
    path('students/<str:email>', students.StudentDetailView.as_view(),
         name='student_details'),

    path('students/password/reset',
         SendPasswordResetEmail.as_view(), name='SendPasswordResetEmail'),
    path('students/password/reset/<token>',
         ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('students/check-in/', attendance.AttendanceRecordsAPIView.as_view(),
         name='attendance_checkin'),
    path('students/check-out/', attendance.AttendanceCheckoutApiView.as_view(),
         name='attendance_checkout'),

    path('students/singleuser/registration', SingleUserRegistrationView.as_view(),
         name='SingleUserRegistration'),

    path('students/verify/<str:token>', StudentVerificationAPIVIew.as_view(),
         name='student_verification'),

    path('comments/<int:record_id>', comments_views.CommentListAPIView.as_view(),
          name='list_attendance_records_comments'),
    path('create_comments/', comments_views.CommentsCreatePIView.as_view(),
         name='create_attendance_records_comments'),
    path('comment/<int:id>', comments_views.CommentRetrieveUpdateDestroy.as_view(),
         name='retrieve_attendance_records_comment'),

    path('students/attendance-records/', attendance.RetrieveAttendanceRecordsView.as_view(),
         name='attendance_records')
]
