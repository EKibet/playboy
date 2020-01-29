from . import views
from django.conf.urls import url
from django.urls import path, include
from .views import SendEmails

app_name = 'staff'

urlpatterns = [
    path(r'api/staff/', views.StaffListing.as_view(), name = 'stafflist'),
    path('staff/send-mail', SendEmails.as_view(), name='send-mail')
]
