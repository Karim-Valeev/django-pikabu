from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from .base import BaseModel


class UserManager(DjangoUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects: UserManager = UserManager()

    email = models.EmailField(unique=True, null=False, blank=False, verbose_name="Email")
    username = models.CharField(
        unique=True, max_length=25, null=False, blank=False, default="Unknown", verbose_name="Username"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        db_table = "account"
        verbose_name = "User"
        verbose_name_plural = "Users"
