
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='auth_users')
    user_permissions = models.ManyToManyField(Permission, related_name='auth_users')
    groups = models.ManyToManyField(Group, related_name='register_users')
    user_permissions = models.ManyToManyField(Permission, related_name='register_users')



    def save(self, *args, **kwargs):
        # Hash the passwords before saving the user
        self.password = make_password(self.password)
        self._password2 = make_password(self._password2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

