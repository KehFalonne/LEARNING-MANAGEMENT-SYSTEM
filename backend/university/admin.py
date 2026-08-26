from django.contrib import admin

from .models import (
    University,
    Faculty,
    Department,
    Programme,
    Level,
    AcademicSession,
    Semester,
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "email",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "university",
        "is_active",
    )

    list_filter = (
        "university",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "faculty",
        "is_active",
    )

    list_filter = (
        "faculty",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "faculty__name",
        "faculty__code",
    )


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "department",
        "degree_type",
        "duration_years",
        "is_active",
    )

    list_filter = (
        "degree_type",
        "department",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "department__name",
        "department__code",
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "programme",
        "order",
        "is_active",
    )

    list_filter = (
        "programme",
        "is_active",
    )

    search_fields = (
        "name",
        "programme__name",
        "programme__code",
    )

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "is_current",
    )
    search_fields = (
    "name",
    )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "academic_session",
        "name",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "academic_session",
        "name",
        "is_current",
    )
    search_fields = (
    "academic_session__name",
    )

