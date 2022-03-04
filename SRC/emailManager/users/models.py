from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(_('email address'), unique=True)
    recovery_email = models.EmailField(null=True, blank=True, unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'recovery_email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Relation(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    time = models.DateTimeField(auto_now_add=True)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
