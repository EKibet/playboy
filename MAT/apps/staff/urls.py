from django.conf.urls import url
from django.urls import include, path

from . import views
from .views import SendEmails

app_name = 'staff'

urlpatterns = [
    path('staff/send-mail', SendEmails.as_view(), name='send-mail'),
    path('tm/<int:id>/', views.TmDetails.as_view(), name='tm_details'),
]
