from django.contrib import admin

from .models import (
    Course,
    CourseOffering,
    CourseTeachingAssignment,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "title",
        "credit_units",
        "course_type",
        "programme",
        "level",
        "is_active",
    )

    list_filter = (
        "course_type",
        "programme",
        "level",
        "is_active",
    )

    search_fields = (
        "code",
        "title",
        "programme__name",
        "programme__code",
    )

    autocomplete_fields = (
        "programme",
        "level",
    )


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):

    list_display = (
        "course",
        "academic_session",
        "semester",
        "is_active",
    )

    list_filter = (
        "academic_session",
        "semester",
        "is_active",
    )

    search_fields = (
        "course__code",
        "course__title",
    )

    autocomplete_fields = (
        "course",
        "academic_session",
        "semester",
    )


@admin.register(CourseTeachingAssignment)
class CourseTeachingAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "course_offering",
        "lecturer",
        "is_primary",
        "assigned_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "course_offering__course__code",
        "course_offering__course__title",
        "lecturer__staff_id",
        "lecturer__user__first_name",
        "lecturer__user__last_name",
    )

    autocomplete_fields = (
        "course_offering",
        "lecturer",
    )