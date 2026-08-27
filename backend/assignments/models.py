from django.db import models


class Assignment(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"

    course_offering = models.ForeignKey(
        "courses.CourseOffering",
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    lecturer = models.ForeignKey(
        "lecturers.Lecturer",
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    title = models.CharField(
        max_length=255,
    )

    instructions = models.TextField()

    attachment = models.FileField(
        upload_to="assignments/",
        blank=True,
        null=True,
    )

    total_marks = models.PositiveIntegerField(
        default=100,
    )

    due_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return (
            f"{self.course_offering.course.code} - "
            f"{self.title}"
        )


class AssignmentSubmission(models.Model):

    class SubmissionStatus(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        LATE = "LATE", "Late"
        GRADED = "GRADED", "Graded"

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="assignment_submissions",
    )

    file = models.FileField(
        upload_to="assignment_submissions/",
    )

    submitted_at = models.DateTimeField(
        auto_now=True,
    )

    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.SUBMITTED,
    )

    marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    feedback = models.TextField(
        blank=True,
    )

    graded_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "assignment",
                    "student",
                ],
                name="unique_student_assignment_submission",
            )
        ]

    def __str__(self):
        return (
            f"{self.assignment.title} - "
            f"{self.student.student_id}"
        )