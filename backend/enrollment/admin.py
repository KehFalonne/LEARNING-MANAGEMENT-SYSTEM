from django.contrib import admin

from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course_offering",
        "status",
        "registered_at",
    )

    list_filter = (
        "status",
        "course_offering__academic_session",
        "course_offering__semester",
    )

    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
        "course_offering__course__code",
        "course_offering__course__title",
    )

    autocomplete_fields = (
        "student",
        "course_offering",
    )