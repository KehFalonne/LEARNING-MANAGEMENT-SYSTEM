from rest_framework import serializers

from .models import (
    CourseOffering,
    CourseTeachingAssignment,
)


class CourseTeachingAssignmentSerializer(
    serializers.ModelSerializer
):

    lecturer_name = serializers.SerializerMethodField()
    staff_id = serializers.CharField(
        source="lecturer.staff_id",
        read_only=True,
    )

    class Meta:
        model = CourseTeachingAssignment

        fields = (
            "id",
            "lecturer_name",
            "staff_id",
            "is_primary",
        )

    def get_lecturer_name(self, obj):
        return obj.lecturer.user.get_full_name()


class CourseDetailSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(
        source="course.code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    description = serializers.CharField(
        source="course.description",
        read_only=True,
    )

    credit_units = serializers.IntegerField(
        source="course.credit_units",
        read_only=True,
    )

    course_type = serializers.CharField(
        source="course.course_type",
        read_only=True,
    )

    semester = serializers.CharField(
        source="semester.name",
        read_only=True,
    )

    academic_session = serializers.CharField(
        source="academic_session.name",
        read_only=True,
    )

    lecturers = CourseTeachingAssignmentSerializer(
        source="teaching_assignments",
        many=True,
        read_only=True,
    )

    class Meta:
        model = CourseOffering

        fields = (
            "id",
            "course_code",
            "course_title",
            "description",
            "credit_units",
            "course_type",
            "semester",
            "academic_session",
            "lecturers",
            "is_active",
        )