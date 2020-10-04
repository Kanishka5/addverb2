from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

# employee table


class Employee(AbstractUser):
    username = models.CharField(blank=False, max_length=20,unique=True)
    name = models.CharField(
        blank=False, max_length=50, default='admin')
    mobile = models.CharField(blank=False, max_length=10, default="0000000000")

    def __str__(self):
        return self.name

    def publish(self):
        self.save()
