from django.urls import path

from .views import ProfileDetail, ProfileListView

"""
Django 2.0 requires the app_name variable set when using include namespace
"""
app_name = 'profiles'

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='all_profiles'),
    path('profiles/<int:id>/', ProfileDetail.as_view(), name='profile_details'),
]
