from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, max_length=255, unique=True)

    name = models.CharField(max_length=255, default='Default Name')

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
