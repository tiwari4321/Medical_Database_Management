# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class UserManager(BaseUserManager):

    def create_user(self,email,password=None,is_active=True,is_researcher = False, is_doctor = False ,is_staff=False, is_admin= False):
        if not email:
            raise ValueError("User must have a valid email address")
        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_researcher = is_researcher
        user_obj.is_doctor = is_doctor
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.save(using=self._db)
        return  user_obj


    def create_staffuser(self,email,password):
        user = self.create_user(
            email,
            password,
            is_staff=True
        )
        return user


    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,
            password,
            is_admin=True,
            is_staff=True
        )

        return user


class User(AbstractBaseUser):
    email = models.EmailField(

        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_researcher = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return  self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

