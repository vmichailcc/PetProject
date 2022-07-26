from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserManager(BaseUserManager):
#     def create_user(self, email,  first_name, last_name, city, password=None, is_admin=False, is_staff=False,
#                     is_active=True):
#         if not email:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not password:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not first_name:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not last_name:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not city:
#             raise ValueError("Користувач повинен заповнити це поле!")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.first_name = first_name
#         user.last_name = last_name
#         user.city = city
#         user.set_password(password)
#         user.admin = is_admin
#         user.staff = is_staff
#         user.active = is_active
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email,  first_name, last_name, city, password=None):
#         if not email:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not password:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not first_name:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not last_name:
#             raise ValueError("Користувач повинен заповнити це поле!")
#         if not city:
#             raise ValueError("Користувач повинен заповнити це поле!")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.first_name = first_name
#         user.last_name = last_name
#         user.city = city
#         user.set_password(password)
#         user.admin = True
#         user.staff = True
#         user.active = True
#         user.save(using=self._db)
#         return user
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    city = models.CharField(verbose_name="Місто", max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    username = models.EmailField(max_length=254, null=True)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = UserManager()
