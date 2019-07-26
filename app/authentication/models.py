from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField('Student', default=True,)
    is_teacher = models.BooleanField('Instructor', default=False)

    def __str__(self):
        return '<User {}>'.format(self.email)
