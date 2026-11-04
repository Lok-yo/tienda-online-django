from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email and username:
            email = f"{username}@utslrc.edu.mx"
        if not username and email:
            username = email.split("@")[0]
        return super().create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        if not email and username:
            email = f"{username}@utslrc.edu.mx"
        if not username and email:
            username = email.split("@")[0]
        return super().create_superuser(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    matricula = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Matrícula",
    )
    carrera = models.CharField(
        max_length=100,
        blank=True,
        default="IDGS",
        verbose_name="Carrera",
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        default="",
        verbose_name="Teléfono",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["id"]

    def __str__(self):
        return f"{self.email} ({self.matricula or self.username})"
