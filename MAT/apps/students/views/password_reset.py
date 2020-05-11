from datetime import timedelta, datetime

import jwt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import User
from MAT.apps.common.utility import send_link
from MAT.config.settings.base import env


class SendPasswordResetEmail(APIView):
    """
    Allows users to send password reset requests
    Args:
        email: The email ssociated with the account
    """
    permission_classes = (AllowAny,)

    def post(self, request):

        try:
            provided_email = request.data.get('email')

            user = User.objects.get(email=provided_email)
            email = user.email

            subject = 'Password Reset'
            message = 'Your password reset request has been received '

            recipient = [email]
            payload = {'email': recipient,
                       "iat": datetime.now(),
                       "exp": datetime.utcnow()
                              + timedelta(minutes=20)
                       }
            token = jwt.encode(payload,
                               env.str('SECRET_KEY'),
                               algorithm='HS256').decode('utf-8')
            url = '/confirm-password/{}'.format(token)

            template = 'password_reset.html'

            kwargs = {"email": email, "subject": subject, "template": template,
                      "url": url, "token": token}
            send_link(**kwargs)

            message = {
                "message": "email has been successfully sent",
                "token": token
            }
            return Response(message, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            message = {
                "message": "This email does not exist"
            }

        return Response(message, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    """
    Allows users to reset their account passwords
    Args:
        password: The new account password
        confirm_password: Has to match the new account password
    """
    permission_classes = (AllowAny,)

    def put(self, request, token):
        try:
            decoded = jwt.decode(token, env.str(
                'SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(email=decoded['email'][0])
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')

            if password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                message = {
                    "message": "Password has been confirmed"
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {
                    "message": "The passwords do not match"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:  # pragma: no cover
            message = {
                'message': 'User does not exist'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
