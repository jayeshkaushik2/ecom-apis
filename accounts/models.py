from enum import unique
from lib2to3.pytree import Base
from signal import raise_signal
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_filepath(self, filename):
    return f"profile_images/{self.pk}/banner.png"


def get_banner_filepath(self, filename):
    return f"banner_images/{self.pk}/banner.png"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    mobile = PhoneNumberField()
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to=get_profile_filepath, null=True, blank=True
    )
    banner_image = models.ImageField(
        upload_to=get_banner_filepath, null=True, blank=True
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_lable) -> bool:
        return True

    def is_staff_user(self) -> bool:
        return self.is_staff

    def is_superuser_user(self) -> bool:
        return self.is_superuser

    def is_staff_or_manager_user(self) -> bool:
        return self.is_staff or self.is_manager


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    banner_image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    alternate_phone = PhoneNumberField(null=True, blank=True)
    pincode = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    area_info = models.TextField(null=True, blank=True)
    house_info = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=256, null=True, blank=True)
    ref = models.UUIDField(null=True, blank=True, unique=True)


class UserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=256, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    counter = models.PositiveBigIntegerField(default=0, null=True, blank=True)

    def update_count(self):
        self.counter += 1
        self.save()


class UserPhone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    counter = models.PositiveBigIntegerField(default=0, null=True, blank=True)

    def update_count(self):
        self.counter += 1
        self.save()
