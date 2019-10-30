from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from classroom.models import (
    Problem,
    ProblemUserMembership,
)
from classroom.serializers import (
    SimpleProblemSerializer,
    ProblemUserMembershipSerializer,
)
from classroom.permissions import (
    UserIsCourseMember,
    UserIsTeacher,
    SafeOnly,
)


class ProblemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SimpleProblemSerializer
    permission_classes = (
        UserIsCourseMember,
        UserIsTeacher|SafeOnly,
    )

    def get_queryset(self):
        lecture_id = self.kwargs.get('lecture_pk')
        return Problem.objects.filter(lecture__id=lecture_id)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            course_id=self.kwargs.get('course_pk'), 
            lecture_id=self.kwargs.get('lecture_pk'), 
        )


class DoneProblemListAPIView(generics.ListAPIView):
    serializer_class = ProblemUserMembershipSerializer
    permission_classes = (
        UserIsTeacher,
        UserIsCourseMember,
    )

    def get_queryset(self):
        lecture_id = self.kwargs.get('lecture_pk')
        queryset = ProblemUserMembership.objects.filter(
            problem__in = Problem.objects.filter(lecture__id=lecture_id),
            done_status = True,
        )
        return queryset


class DoneProblemRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = ProblemUserMembershipSerializer
    permission_classes = (
        UserIsTeacher,
        UserIsCourseMember,
    )    
    
    def get(self, request, *args, **kwargs):
        obj = ProblemUserMembership.objects.get(
            user__username=self.kwargs.get('username'),
            problem__lecture=self.kwargs.get('lecture_pk'),
        )
        serializer = ProblemUserMembershipSerializer(obj)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class DoneProblemMarkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProblemUserMembershipSerializer
    permission_classes = (
        UserIsTeacher,
        UserIsCourseMember,
    )

    def update(self, request, *args, **kwargs):
        obj = ProblemUserMembership.objects.get(
            user__username=self.kwargs.get('username'),
            problem__lecture=self.kwargs.get('lecture_pk'),
        )
        obj.mark = request.data.get('mark')
        obj.accept_status = True
        obj.save()
        serializer = ProblemUserMembershipSerializer(obj)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

