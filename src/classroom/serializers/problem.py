import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from classroom.models import (
    Course,
    Lecture,
    Problem,
    ProblemUserMembership,
)
from accounts.serializers import UserSerializer


class SimpleProblemSerializer(ModelSerializer):
    creator = UserSerializer(read_only=True)
    lecture = serializers.StringRelatedField(read_only=True) 
    
    class Meta:
        model = Problem
        fields = (
            'title',
            'description',
            'date_created',
            'deadline',
            'creator',
            'lecture',
        )

    def validate_deadline(self, deadline):
        if deadline < datetime.today() :
            msg = "Deadline date can't be before created date"
            raise serializers.ValidationError(msg)
        return deadline
        
    def create(self, validated_data):
        creator = validated_data.pop('creator')
        
        lecture_id = validated_data.pop('lecture_id')
        lecture = Lecture.objects.get(id=lecture_id)

        course_id = validated_data.pop('course_id')
        course = Course.objects.get(id=course_id)
        
        problem = Problem.objects.create(
            creator=creator,
            lecture=lecture,
            **validated_data)

        students = course.members.filter(user_type='Student')
        problem.members.add(*list(students)) 

        return problem


class ProblemUserMembershipSerializer(ModelSerializer):
    problem = SimpleProblemSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta: 
        model = ProblemUserMembership
        fields = (
            'id',
            'problem',
            'user',
            'done_status',
            'accept_status',
            'mark',
        )
