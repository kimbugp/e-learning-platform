from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField('Student', default=True,)

    def __str__(self):
        return '<User {}>'.format(self.email)