from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SocialAuthenticationView

from . import views

app_name = "authentication"
urlpatterns = [

    path('login', views.SigninView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/registration',
          views.SingleUserRegistrationView.as_view(),name='SingleUserRegistration'),
    path('auth/logout/', views.SignoutView.as_view(), name="SignoutView"),

    path('login/oauth',
          views.SocialAuthenticationView.as_view(),name='social_auth')

]
