from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView,)
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from .models import UserProfile
from .serializers import ProfileSerializer
from .renderers import (ProfileJSONRenderer, ProfilesJSONRenderer)


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfilesJSONRenderer,)

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(user__username=username)
        except:
            message = {"error": "Profile does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        instance_profile = UserProfile.objects.get(user__username=username)
        data = request.data
        serializer = self.serializer_class(
            instance=instance_profile, data=data, partial=True,
            context={
                'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
