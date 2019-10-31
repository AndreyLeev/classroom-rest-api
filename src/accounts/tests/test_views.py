import json

from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User


class UserRegistrationAPIViewTest(APITestCase):
    url = reverse('accounts:registration')

    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "user_type": "Student",
            "password": "123test123",
            "confirm_password": "123test123",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_invalid_password(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "user_type": "Student",
            "password": "123test123",
            "confirm_password": "INVALID",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    
class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("accounts:login")

    def setUp(self):
        self.username = "testuser"
        self.password = "123test123"
        self.user_type = "Student"
        self.user = User(
            username=self.username,
            user_type=self.user_type,
        )
        self.user.set_password(self.password)
        self.user.save()
        self.token = Token.objects.create(user=self.user)
    
    def tearDown(self):
        self.user.delete()
        self.token.delete()

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "testuser"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        user_data = {"username": self.username, "password": "INVALID"}
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        content = json.loads(response.content)      
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in content)
        self.assertEqual(content["token"], self.token.key)


class UserTokenAPIViewTestCase(APITestCase):
    
    def url(self, key):
        return reverse("accounts:token", kwargs={"key": key})

    def setUp(self):
        self.username = "testuser"
        self.password = "123test123"
        self.user_type = "Student"
        self.user = User.objects.create(
            username=self.username,
            user_type=self.user_type,
            password=self.password
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def tearDown(self):
        self.user.delete()
        self.token.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_delete_by_key(self):
        response = self.client.delete(self.url(self.token.key))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_current(self):
        response = self.client.delete(self.url('current'))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_retrive_by_key(self):
        response = self.client.get(self.url(self.token.key))
        self.assertEqual(200, response.status_code)

    def test_retrive_current(self):
        response = self.client.get(self.url('current'))
        self.assertEqual(200, response.status_code)