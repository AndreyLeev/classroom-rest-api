from rest_framework import generics

from classroom.models import (
    ProblemUserMembership,
    ProblemSolution,
)
from classroom.serializers import (
    ProblemUserMembershipSerializer,
    SolutionSerializer,
)
from classroom.permissions import (
    UserIsStudent,
    UserIsOwner,
)


class UserProblemListAPIView(generics.ListAPIView):
    serializer_class = ProblemUserMembershipSerializer
    permission_classes = (
        UserIsStudent,
    )    
    
    def get_queryset(self):
        queryset = ProblemUserMembership.objects.filter(
            user=self.request.user.id
        )
        return queryset


class UserProblemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProblemUserMembershipSerializer
    queryset = ProblemUserMembership.objects.all()
    permission_classes = (
        UserIsStudent,
        UserIsOwner,
    )


class UserProblemSolutionAPIView(generics.ListCreateAPIView):
    serializer_class = SolutionSerializer
    permission_classes = (
        UserIsStudent,
        UserIsOwner,
    )

    def get_queryset(self):
        problem_id = self.kwargs.get('pk')
        return ProblemSolution.objects.filter(problem=problem_id)

    def perform_create(self, serializer):
        serializer.save(problem_id=self.kwargs.get('pk'))

