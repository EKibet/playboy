from django.conf.urls import url
from django.urls import include, path

from . import views
from .views import SendEmails

app_name = 'staff'

urlpatterns = [
    path('api/staff/', views.StaffListing.as_view(), name = 'stafflist'),
    path('staff/send-mail', SendEmails.as_view(), name='send-mail')
]
