from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.common.utility import make_cloudinary_url

from .models import UserProfile
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfilesJSONRenderer,)

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, id):
        try:
            profile = UserProfile.objects.get(user__id=id)
        except:
            message = {"error": "Profile does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        instance_profile = UserProfile.objects.get(user__id=id)
        if instance_profile.user.id != request.user.id:
            data = {'error': 'You are not allowed to edit another persons profile'}
            return Response(data, status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(
            instance=instance_profile, data=data, partial=True,
            context={
                'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.FILES:
            profile_picture = request.FILES["profile_picture"]
            secure_url = make_cloudinary_url(
                profile_picture, request.user.username)
            instance_profile.image = secure_url
            instance_profile.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
