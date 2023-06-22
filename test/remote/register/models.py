# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='auth_users', related_query_name='auth_user_user')
    user_permissions = models.ManyToManyField(Permission, related_name='auth_users', related_query_name='auth_user_user')

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password2 = models.CharField(max_length=128, null=True)

    def save(self, *args, **kwargs):
        # Hash the passwords before saving the user
        self.password = make_password(self.password)
        self.password2 = make_password(self.password2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
