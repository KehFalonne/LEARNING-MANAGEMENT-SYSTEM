from django.conf import settings
from django.db import models

from university.models import Programme, Level


class Student(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        GRADUATED = "GRADUATED", "Graduated"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    student_id = models.CharField(
        max_length=30,
        unique=True,
    )

    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="students",
    )

    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        related_name="students",
    )

    admission_year = models.PositiveIntegerField()

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    guardian_name = models.CharField(
        max_length=150,
        blank=True,
    )

    guardian_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"