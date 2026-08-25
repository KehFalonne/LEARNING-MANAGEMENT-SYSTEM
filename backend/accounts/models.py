from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        LECTURER = "LECTURER", "Lecturer"
        STUDENT = "STUDENT", "Student"
        STAFF = "STAFF", "Staff"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to = "profile_picture",
        blank = True,
        null = True,
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    