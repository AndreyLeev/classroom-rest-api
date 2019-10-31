from rest_framework.serializers import ModelSerializer

from classroom.models import (
    ProblemUserMembership,
    Comment,
)
from accounts.serializers import UserSerializer

class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
   
    class Meta:
        model = Comment
        fields = (
            'user',
            'text',
            'date_created',
        )

    def create(self, validated_data):
        problem_id = validated_data.pop('problem_id')
        user = validated_data.pop('user')
        problem = ProblemUserMembership.objects.get(id=problem_id)
        comment = Comment.objects.create(
            user=user,
            problem=problem,
            **validated_data
        )
        return comment