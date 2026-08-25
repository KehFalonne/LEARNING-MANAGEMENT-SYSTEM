from django.db import models


class University(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    address = models.TextField(blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    logo = models.ImageField(
        upload_to="university/",
        blank=True,
        null=True,
    )

    website = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Faculty(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="faculties",
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["university", "code"],
                name="unique_faculty_code_per_university",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "code"],
                name="unique_department_code_per_faculty",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Programme(models.Model):
    class DegreeType(models.TextChoices):
        CERTIFICATE = "CERTIFICATE", "Certificate"
        DIPLOMA = "DIPLOMA", "Diploma"
        BACHELOR = "BACHELOR", "Bachelor's Degree"
        MASTER = "MASTER", "Master's Degree"
        DOCTORATE = "DOCTORATE", "Doctorate"

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programmes",
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)

    degree_type = models.CharField(
        max_length=20,
        choices=DegreeType.choices,
    )

    duration_years = models.PositiveIntegerField(default=4)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_programme_code_per_department",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Level(models.Model):
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name="levels",
    )

    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["programme", "name"],
                name="unique_level_per_programme",
            )
        ]

    def __str__(self):
        return f"{self.programme.code} - {self.name}"


class AcademicSession(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_current = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Semester(models.Model):
    class SemesterType(models.TextChoices):
        FIRST = "FIRST", "First Semester"
        SECOND = "SECOND", "Second Semester"

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="semesters",
    )

    name = models.CharField(
        max_length=20,
        choices=SemesterType.choices,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_current = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["academic_session", "name"],
                name="unique_semester_per_session",
            )
        ]

    def __str__(self):
        return f"{self.academic_session.name} - {self.get_name_display()}"