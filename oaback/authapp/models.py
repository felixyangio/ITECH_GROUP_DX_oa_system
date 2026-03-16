from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email cannot be empty')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    realname = models.CharField(max_length=50, verbose_name='Full Name')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff Status')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['realname']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.realname}({self.email})'
