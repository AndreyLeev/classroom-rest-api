from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from classroom.models import (
    Course,
    Problem
) 
from classroom.serializers import (
    CourseSerializer,
    UserSerializer,
)
from classroom.permissions import (
    UserIsCourseMember,
    UserIsTeacher,
    SafeOnly,
)

User = get_user_model()

class CourseListCreateAPIView(generics.ListCreateAPIView):
    """
        API endpoint for listing and creating courses.
        Courses queryset is filter for appropriate user.   
    """
    serializer_class = CourseSerializer 
    permission_classes = (
        UserIsTeacher|SafeOnly,
    )

    def get_queryset(self):
        return Course.objects.filter(
            members__id=self.request.user.id
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = CourseSerializer
    queryset = Course.objects.all() 
    permission_classes = (
        UserIsCourseMember,
        UserIsTeacher|SafeOnly,
    )
    lookup_url_kwarg = 'course_pk'


class CourseMembersListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for adding, listing and removing members."""

    serializer_class = UserSerializer
    permission_classes = (
        UserIsTeacher,
        UserIsCourseMember,
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'user_type',]

    def get_queryset(self):
        course = Course.objects.get(
            id = self.kwargs.get('course_pk')
        )
        return course.members.all()

    def post(self, request, *args, **kwargs):
        """Add a user instance to the course members."""
        username = request.data.get('username')
        course = get_object_or_404(
            Course.objects.all(),
            id=self.kwargs.get('course_pk')
        )       
        user = get_object_or_404(
            User.objects.all(),
            username=username
        )
        course.members.add(user)

        # Add all course problems to new student 
        if user.is_student:
            problems = Problem.objects.filter(
                lecture__course__id=course.id
            )
            user.problem_set.add(*list(problems))
            
        return Response(
            data=CourseSerializer(course).data,
            status=status.HTTP_200_OK,
        )


class CourseMembersDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (
        UserIsTeacher,
        UserIsCourseMember,
    )
    lookup_url_kwarg = 'username'

    def delete(self, request, *args, **kwargs):
        """Remove student from course members."""
        course = get_object_or_404(
            Course.objects.all(),
            id=self.kwargs.get('course_pk')
        )
        user = get_object_or_404(
            User.objects.all(),
            username=self.kwargs.get('username')
        )
        if user.is_student:
            course.members.remove(user)

            # Remove all course problems from student
            problems = Problem.objects.filter(
                lecture__course__id=course.id
            )
            user.problem_set.remove(*list(problems))

            return Response(
                data=CourseSerializer(course).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message':'User must be a student.'},
                status=status.HTTP_400_BAD_REQUEST
            )
