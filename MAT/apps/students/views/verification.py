import os

import jwt
from rest_framework import generics, exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MAT.apps.authentication.models import User
from MAT.apps.students.renderers import StudentJSONRenderer
from MAT.apps.students.serializers import StudentSerializer


class StudentVerificationAPIVIew(generics.GenericAPIView):
    serializer_class = StudentSerializer
    # by this time the student will not be able to login,
    # therefore lets allow unauthenticated  requests for this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (StudentJSONRenderer,)

    def get(self, request, token):
        """
        Given a token, we decode the token get the user and activate him/her
        """
        try:
            payload = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            msg = "Token has expired, please generate a new one"
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding token, please generate a new one.'
            raise exceptions.AuthenticationFailed(msg)
        # get the user then check if he is verified
        user = User.objects.get(pk=payload['user_id'])

        # first check if the user is verified
        if user.is_verified == False:
            user.is_verified = True
            user.save()
            return Response({"message": "account verified successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "You have already verified your account"}, status=status.HTTP_400_BAD_REQUEST)
