from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, help_text=" Enter user name")
    email = models.EmailField()
    password = models.CharField(max_length=30)
    new_password = models.CharField(max_length=30)

    objects = UserManager()

    def __str__(self):
        return self.username