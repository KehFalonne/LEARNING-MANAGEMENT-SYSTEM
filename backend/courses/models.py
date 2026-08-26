from django.db import models

from university.models import (
    Programme,
    Level,
    AcademicSession,
    Semester,
)


class Course(models.Model):

    class CourseType(models.TextChoices):
        CORE = "CORE", "Core"
        ELECTIVE = "ELECTIVE", "Elective"
        GENERAL = "GENERAL", "General"

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    credit_units = models.PositiveIntegerField()

    course_type = models.CharField(
        max_length=20,
        choices=CourseType.choices,
        default=CourseType.CORE,
    )

    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class CourseOffering(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="offerings",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="course_offerings",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="course_offerings",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course",
                    "academic_session",
                    "semester",
                ],
                name="unique_course_offering",
            )
        ]

    def __str__(self):
        return (
            f"{self.course.code} - "
            f"{self.academic_session.name} - "
            f"{self.semester.get_name_display()}"
        )


class CourseTeachingAssignment(models.Model):

    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.CASCADE,
        related_name="teaching_assignments",
    )

    lecturer = models.ForeignKey(
        "lecturers.Lecturer",
        on_delete=models.PROTECT,
        related_name="course_assignments",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course_offering",
                    "lecturer",
                ],
                name="unique_lecturer_course_offering",
            )
        ]

    def __str__(self):
        return (
            f"{self.course_offering.course.code} - "
            f"{self.lecturer.staff_id}"
        )