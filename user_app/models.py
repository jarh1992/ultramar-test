from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo para gestionar Usuarios
    """

    id_user = models.PositiveIntegerField("Id User", null=False, blank=False, unique=True, default=0)
    first_name = models.CharField("First Name", max_length=30, blank=False, null=False, default='first name')
    last_name = models.CharField("Last Name", max_length=30, blank=False, null=False, default='last name')
    email = models.EmailField("Email", unique=True)
    username = models.CharField("Username", max_length=100, blank=False, null=False, unique=True)
    password = models.CharField("Passwors", max_length=100)

    def __str__(self):
        return self.username
