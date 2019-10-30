from rest_framework import generics

from classroom.models import Lecture 
from classroom.serializers import LectureSerializer
from classroom.permissions import (
    UserIsCourseMember,
    UserIsTeacher,
    SafeOnly,
)

class LectureListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = LectureSerializer
    permission_classes = (
        UserIsCourseMember,
        UserIsTeacher|SafeOnly,
    )

    def get_queryset(self):
        user = self.request.user
        return Lecture.objects.filter(course__members__id=user.id)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            course_id=self.kwargs.get('course_pk'),
        )

class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    permission_classes = (
        UserIsCourseMember,
        UserIsTeacher|SafeOnly,
    )
    lookup_url_kwarg = 'lecture_pk'