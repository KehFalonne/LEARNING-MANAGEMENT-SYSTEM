from django.contrib import admin

from .models import (
    Course,
    CourseOffering,
    CourseTeachingAssignment,
    LearningMaterial,
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


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course_offering",
        "material_type",
        "week",
        "uploaded_by",
        "is_published",
        "created_at",
    )

    list_filter = (
        "material_type",
        "is_published",
        "course_offering__academic_session",
        "course_offering__semester",
    )

    search_fields = (
        "title",
        "description",
        "course_offering__course__code",
        "course_offering__course__title",
        "uploaded_by__staff_id",
        "uploaded_by__user__first_name",
        "uploaded_by__user__last_name",
    )

    autocomplete_fields = (
        "course_offering",
        "uploaded_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )