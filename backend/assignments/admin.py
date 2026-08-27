from django.contrib import admin

from .models import (
    Assignment,
    AssignmentSubmission,
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course_offering",
        "lecturer",
        "total_marks",
        "due_date",
        "status",
    )

    list_filter = (
        "status",
        "course_offering__academic_session",
        "course_offering__semester",
    )

    search_fields = (
        "title",
        "course_offering__course__code",
        "course_offering__course__title",
        "lecturer__staff_id",
    )

    autocomplete_fields = (
        "course_offering",
        "lecturer",
    )


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "assignment",
        "student",
        "status",
        "submitted_at",
        "marks",
        "graded_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "assignment__title",
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
    )

    autocomplete_fields = (
        "assignment",
        "student",
    )

    readonly_fields = (
        "submitted_at",
        "graded_at",
    )