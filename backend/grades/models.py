from django.db import models

from students.models import Student
from courses.models import CourseOffering


class Grade(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    coursework_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    exam_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    total_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    grade = models.CharField(
        max_length=2,
        blank=True,
    )

    grade_point = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    remarks = models.CharField(
        max_length=100,
        blank=True,
    )

    is_released = models.BooleanField(
        default=False,
    )

    released_at = models.DateTimeField(
        blank=True,
        null=True,
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
                    "student",
                    "course_offering",
                ],
                name="unique_student_course_grade",
            )
        ]

        ordering = [
            "course_offering__course__code",
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.course_offering.course.code}"
        )

    def calculate_result(self):
        """
        Calculate total, grade, grade point
        and remarks.
        """

        self.total_marks = (
            self.coursework_marks +
            self.exam_marks
        )

        if self.total_marks >= 80:
            self.grade = "A"
            self.grade_point = 4.00
            self.remarks = "Excellent"

        elif self.total_marks >= 70:
            self.grade = "B"
            self.grade_point = 3.00
            self.remarks = "Very Good"

        elif self.total_marks >= 60:
            self.grade = "C"
            self.grade_point = 2.00
            self.remarks = "Good"

        elif self.total_marks >= 50:
            self.grade = "D"
            self.grade_point = 1.00
            self.remarks = "Pass"

        elif self.total_marks >= 40:
            self.grade = "E"
            self.grade_point = 0.00
            self.remarks = "Pass"

        else:
            self.grade = "F"
            self.grade_point = 0.00
            self.remarks = "Fail"

    def save(self, *args, **kwargs):
        self.calculate_result()
        super().save(*args, **kwargs)