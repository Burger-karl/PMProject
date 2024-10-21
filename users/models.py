from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=11, choices=USER_TYPE_CHOICES, default='client')
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

