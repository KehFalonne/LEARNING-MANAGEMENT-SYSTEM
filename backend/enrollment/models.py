from django.db import models


class Enrollment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DROPPED = "DROPPED", "Dropped"
        COMPLETED = "COMPLETED", "Completed"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    course_offering = models.ForeignKey(
        "courses.CourseOffering",
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    registered_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-registered_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "course_offering",
                ],
                name="unique_student_course_enrollment",
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.course_offering.course.code}"
        )