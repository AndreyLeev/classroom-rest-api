from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from classroom.models import (
    ProblemSolution,
    ProblemUserMembership,
)

class SolutionSerializer(ModelSerializer):

    class Meta:
        model = ProblemSolution
        fields = (
            'solution',
            'date_created',
        )
    
    def create(self, validated_data):
        problem_id = validated_data.pop('problem_id')
        problem = ProblemUserMembership.objects.get(id=problem_id)
        if problem.done_status == True: 
            raise serializers.ValidationError('Solution is already exist')    
        problem.done_status = True
        problem.save()
        solution = ProblemSolution.objects.create(
            problem=problem,
            **validated_data
        )
        return solution
        