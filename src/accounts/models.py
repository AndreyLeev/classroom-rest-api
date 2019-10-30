from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   USER_TYPES = (
      ('Student', 'Student'),
      ('Teacher', 'Teacher'),
   )
   user_type = models.CharField(choices=USER_TYPES, max_length=10)

   @property
   def is_teacher(self):
      return self.user_type == 'Teacher'
   
   @property
   def is_student(self):
      return self.user_type == 'Student'
