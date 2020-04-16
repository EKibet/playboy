from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status


from .models import AttendanceComment, AttendanceRecords
from .serializers import AttendanceCommentSerializer
from .renderers import CommentJSONRenderer
from MAT.apps.authentication.models import User


class CommentsCreatePIView(APIView):
    serializer_class = AttendanceCommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tag = request.data.get('tag')
        relevant_date = request.data.get('relevant_date')

        if tag == 'absent':
            is_present, is_late = False, False
        else:
            is_late, is_present = True, True
        user = User.objects.filter(id=request.user.id).first()
        record = AttendanceRecords.objects.get_or_create(user_id=user, date=relevant_date)[0]
        record.is_late = is_late
        record.is_present = is_present
        record.save()
        
        serializer = self.serializer_class(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=self.request.user, record=record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentListAPIView(ListAPIView):
    serializer_class = AttendanceCommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        record_id = kwargs.get('record_id')
        comments = AttendanceComment.objects.filter(record=record_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class = AttendanceCommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = AttendanceComment.objects.all()
    lookup_field = 'id'
