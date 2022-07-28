from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        username = None
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(verbose_name="Ім'я", max_length=100)
    last_name = models.CharField(verbose_name="Прізвище", max_length=100)
    city = models.CharField(verbose_name="Місто", max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True)
    email_verify = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


