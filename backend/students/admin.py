from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "student_id",
        "user",
        "programme",
        "level",
        "admission_year",
        "status",
    )

    list_filter = (
        "status",
        "programme",
        "level",
        "gender",
    )

    search_fields = (
        "student_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    autocomplete_fields = (
        "user",
        "programme",
        "level",
    )