from rest_framework import serializers

from .models import Enrollment


class StudentEnrollmentSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(
        source="course_offering.course.code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="course_offering.course.title",
        read_only=True,
    )

    credit_units = serializers.IntegerField(
        source="course_offering.course.credit_units",
        read_only=True,
    )

    semester = serializers.CharField(
        source="course_offering.semester.name",
        read_only=True,
    )

    academic_session = serializers.CharField(
        source="course_offering.academic_session.name",
        read_only=True,
    )

    class Meta:
        model = Enrollment

        fields = (
            "id",
            "course_code",
            "course_title",
            "credit_units",
            "semester",
            "academic_session",
            "status",
            "registered_at",
        )