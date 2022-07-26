from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email,  first_name, last_name, city, password=None, is_admin=False, is_staff=False,
                    is_active=True):
        if not email:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not password:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not first_name:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not last_name:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not city:
            raise ValueError("Користувач повинен заповнити це поле!")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.city = city
        user.set_password(password)
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  first_name, last_name, city, password=None, **extra_fields):
        if not email:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not password:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not first_name:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not last_name:
            raise ValueError("Користувач повинен заповнити це поле!")
        if not city:
            raise ValueError("Користувач повинен заповнити це поле!")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.city = city
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(verbose_name="Ім'я", max_length=100)
    last_name = models.CharField(verbose_name="Прізвище", max_length=100)
    city = models.CharField(verbose_name="Місто", max_length=100)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "city"]

    objects = UserManager()
