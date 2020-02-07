from . import views
from django.conf.urls import url
from django.urls import path, include


app_name = 'staff'

urlpatterns = [
    path(r'api/staff/', views.StaffListing.as_view(), name = 'stafflist')
]