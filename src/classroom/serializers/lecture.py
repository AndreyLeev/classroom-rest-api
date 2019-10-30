from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from classroom.models import (
    Course,
    Lecture,
)


class LectureSerializer(ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Lecture
        fields = (
            'id',
            'title',
            'description',
            'date_created',
            'creator',
            'course',
            'file',
        )
    
    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        creator = validated_data.pop('creator')
        course = Course.objects.get(id=course_id)
        lecture = Lecture.objects.create(
            creator=creator,
            course=course,
            **validated_data)
        return lecture
