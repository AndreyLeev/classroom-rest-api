from rest_framework import generics

from classroom.models import Comment
from classroom.serializers import CommentSerializer
from classroom.permissions import UserIsTeacher, UserIsCourseMember, UserIsProblemMember

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (
        UserIsTeacher|UserIsProblemMember,
    )

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_pk')
        return Comment.objects.filter(problem=problem_id)

    def perform_create(self, serializer):
        serializer.save(
            problem_id=self.kwargs.get('problem_pk'),
            user=self.request.user,
        )
