import csv

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from MAT.apps.common.utility import make_cloudinary_url
from MAT.apps.students.utility_functions import calculate_student_attendance
from MAT.apps.common.permissions import IsPodLeaderOrAdmin
from .models import StudentProfile, StudentCurrentTrack
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer

class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfilesJSONRenderer,)

    def get_queryset(self):
        queryset = StudentProfile.objects.all()
        return queryset


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, id):
        try:
            profile = StudentProfile.objects.get(user__id=id)
        except:
            message = {"error": "Profile does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance=profile, context={'request': request})
        response = {'data': serializer.data,
                'attendance': calculate_student_attendance(serializer.data['user'])}
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, id):
        instance_profile = StudentProfile.objects.get(user__id=id)
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


class UploadStudentTrack(APIView):
    """
        View to list all users in the system.

        * Requires token authentication.
        * Only podleaders or admins are able to access this view.
    """
    parser_classes = (FileUploadParser,)
    serializer = ProfileSerializer
    permission_classes =[IsPodLeaderOrAdmin]  

    def patch(self, request, format=None):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = list(csv.DictReader(decoded_file))
        unsuccessful_emails = []
        successful_emails = []
        stats = {
            'updated_count': 0,
            'error_count': 0,
            'unsuccessful_track_update': unsuccessful_emails,
            'successful_track_update': successful_emails,
        }

        try:
            for row in reader:
                try:
                    # get the students profile instance using email
                    profile = StudentProfile.objects.get(user__email=row.get('email'))
                    
                    # get the track instance from from the StudentCurrentTrack model
                    track, obj = StudentCurrentTrack.objects.get_or_create(track=row.get("track"))
                    # Assign the track to the students track
                    profile.current_track = track
     
                    successful_emails.append(row['email'])
                    stats['updated_count'] += 1
        
                    profile.save()
                except StudentProfile.DoesNotExist:
                    unsuccessful_emails.append(row['email'])
                    stats['error_count'] += 1

            return Response(stats, status=status.HTTP_200_OK)
        except KeyError:
            message = {'error': 'CSV data does not have correct format.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
            
