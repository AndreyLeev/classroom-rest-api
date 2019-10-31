import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from classroom.models import *

User = get_user_model()


class  CourseListCreateAPIViewTestCase(APITestCase):
    url = reverse('classroom:course-list')

    def setUp(self):
        self.student = User.objects.create(
            username="student",
            user_type="Student",
            password=make_password("123student123"),
        )
        self.teacher = User.objects.create(
            username="teacher",
            user_type="Teacher",
            password=make_password("123teacher123"),
        ) 
        self.student_token = Token.objects.create(user=self.student)
        self.teacher_token = Token.objects.create(user=self.teacher)

    def tearDown(self):
        self.student.delete()
        self.teacher.delete()
        self.student_token.delete()
        self.teacher_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_by_student(self):
        self.api_authentication(self.student_token)
        data = {"title": "title", "description": "desc"}
        response = self.client.post(self.url, data)
        self.assertEqual(403, response.status_code)

    def test_create_by_teacher(self):
        self.api_authentication(self.teacher_token)
        data = {"title": "title", "description": "desc"}
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_get_by_member(self):
        self.api_authentication(self.student_token)
        course = Course.objects.create(
            title="title",
            description="desc",
        )
        course.members.add(self.student)
        
        course = Course.objects.create(
            title="title_test",
            description="desc",
        )

        response = self.client.get(self.url)
        content = json.loads(response.content).get('results')

        self.assertEqual(200, response.status_code)
        self.assertTrue(len(content) == \
            Course.objects.filter(members__id=self.student.id).count())
    
    def test_get_by_not_member(self):
        """
        Test to verify member courses list
        """
        self.api_authentication(self.student_token)
        course = Course.objects.create(
            title="title",
            description="desc",
        )
        response = self.client.get(self.url)
        content = json.loads(response.content).get('results')
        self.assertTrue(len(content) == 0)

    
class  CourseDetailAPIViewTestCase(APITestCase):
   
    def url(self, course_id):
        return reverse('classroom:course-detail', kwargs={'course_pk':course_id})

    def setUp(self):
        self.student = User.objects.create(
            username="student",
            user_type="Student",
            password=make_password("123student123"),
        )
        self.teacher = User.objects.create(
            username="teacher",
            user_type="Teacher",
            password=make_password("123teacher123"),
        ) 
        self.student_token = Token.objects.create(user=self.student)
        self.teacher_token = Token.objects.create(user=self.teacher)
        self.course = Course.objects.create(
            title="title",
            description="desc",
        )

    def tearDown(self):
        self.student.delete()
        self.teacher.delete()
        self.student_token.delete()
        self.teacher_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_by_member(self):
        self.api_authentication(self.student_token)
        self.course.members.add(self.student)
        response = self.client.get(self.url(self.course.id))
        self.assertEqual(200, response.status_code)
        self.course.members.remove(self.student)

    def test_get_by_not_member(self):
        teacher = User.objects.create(
            username="teacher_test",
            user_type="Teacher",
            password=make_password("123teacher123"),
        ) 
        teacher_token = Token.objects.create(user=teacher)
        self.api_authentication(teacher_token)
        response = self.client.get(self.url(self.course.id))
        self.assertEqual(403, response.status_code)

    def test_update_by_student_member(self):
        self.api_authentication(self.student_token)
        self.course.members.add(self.student)
        data = {"title": "title", "description": "desc"}
        response = self.client.put(self.url(self.course.id), data)
        self.assertEqual(403, response.status_code)
        self.course.members.remove(self.student)

    def test_update_by_teacher_member(self):
        self.api_authentication(self.teacher_token)
        self.course.members.add(self.teacher)
        data = {"title": "title", "description": "desc"}
        response = self.client.put(self.url(self.course.id), data)
        self.assertEqual(200, response.status_code)
        self.course.members.remove(self.teacher)

    def test_update_by_teacher_not_member(self):
        teacher = User.objects.create(
            username="teacher_test",
            user_type="Teacher",
            password=make_password("123teacher123"),
        ) 
        teacher_token = Token.objects.create(user=teacher)  
        self.api_authentication(teacher_token)
        data = {"title": "title", "description": "desc"}
        response = self.client.put(self.url(self.course.id), data)
        self.assertEqual(403, response.status_code)
