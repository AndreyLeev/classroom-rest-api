from rest_framework import permissions
from classroom.models import Course


class SafeOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class UserIsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class UserIsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_teacher


class UserIsStudent(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.user.is_student


class UserIsCourseMember(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            course = Course.objects.get(id=view.kwargs['course_pk'])
        except Course.DoesNotExist:
            return False
        return course.members.filter(id=request.user.id).exists()

 
