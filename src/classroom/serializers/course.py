from rest_framework.serializers import ModelSerializer

from classroom.models import Course
from accounts.serializers import UserSerializer


class CourseSerializer(ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'date_created',
            'members',
        )
    
    def create(self, validated_data):
        creator = validated_data.pop('creator')
        course = Course.objects.create(**validated_data)
        course.members.add(creator)
        return course
