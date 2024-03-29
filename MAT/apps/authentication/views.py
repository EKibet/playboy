import base64
import os

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from MAT.apps.authentication.models import User
from MAT.config.settings.base import env

from . import models
from .models import User
from .serializers import SignOutSerializer, UserRegistrationSerializer, SocialAuthSerializer, CustomTokenObtainPairSerializer


class SingleUserRegistrationView(generics.CreateAPIView):
    """
    Allows a staff to create single student's account
    Args:
        first_name: the student's first name
        last_name: the student's last name
        username: username that will be indexed by the system
        email: the student's email
        password: The new account password
        role: The user's role either TM,STUDENT, POD_LEADER
    """
    permission_classes =[IsAdminUser]
    serializer_class = UserRegistrationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message= {
            'message': 'User registered  successfully',
            }
        return Response(message, status= status.HTTP_201_CREATED)

class SignoutView(generics.CreateAPIView):
    """Adds a token to the blacklist table upon signout

    Arguments:
        refresh_token {str} -- A valid refresh token generated via login/signup endpoints
    """   
    serializer_class = SignOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data.get('refresh_token')
        success_message= {
            'success': 'User logged out successfully',
            }
        error_message= {
            'error': 'Token is invalid or expired',
            }
        try:
            token = RefreshToken(token)
            token.blacklist()
        except TokenError as error:
            return Response(error_message, status= status.HTTP_400_BAD_REQUEST)
        return Response(success_message, status= status.HTTP_200_OK)



class SocialAuthenticationView(APIView):
    """Social authentication."""
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer

    def post(self, request, *args, **kwargs):
        google_client_id = env.str('GOOGLE_CLIENT_ID')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        request = requests.Request()
        try:
            user = id_token.verify_oauth2_token(token, request, google_client_id)
            if user['iss'] != 'accounts.google.com':raise ValueError('Wrong issuer.')
            if user['aud'] != google_client_id:raise ValueError('invalid client id')
            try:
                user_obj = User.objects.get(email=user['email'])
                refresh = RefreshToken.for_user(user_obj)
                access = refresh.access_token
                message= {
                "access":str(access),
                "refresh":str(refresh)
                }
                return Response(message, status= status.HTTP_200_OK)
            except User.DoesNotExist:
                message= {
                'message': 'user does not exist. Request admin to register',
                }
                return Response(message, status= status.HTTP_401_UNAUTHORIZED)
    
        except ValueError:
            message= {
            'message': 'token is expired or not issued by google',
            }
            return Response(message, status= status.HTTP_401_UNAUTHORIZED)

class SigninView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
