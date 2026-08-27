from django.contrib import admin

from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course_offering",
        "coursework_marks",
        "exam_marks",
        "total_marks",
        "grade",
        "grade_point",
        "remarks",
        "updated_at",
    )

    list_filter = (
        "grade",
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

    readonly_fields = (
        "total_marks",
        "grade",
        "grade_point",
        "remarks",
        "created_at",
        "updated_at",
    )