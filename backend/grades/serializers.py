from rest_framework import serializers

from .models import Grade


from rest_framework import serializers

from .models import Grade


class GradeSerializer(serializers.ModelSerializer):

    student_id = serializers.CharField(
        source="student.student_id",
        read_only=True,
    )

    student_name = serializers.SerializerMethodField()

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
        model = Grade

        fields = (
            "id",
            "student",
            "student_id",
            "student_name",
            "course_offering",
            "course_code",
            "course_title",
            "credit_units",
            "semester",
            "academic_session",
            "coursework_marks",
            "exam_marks",
            "total_marks",
            "grade",
            "grade_point",
            "remarks",
            "is_released",
            "released_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "student_id",
            "student_name",
            "course_code",
            "course_title",
            "credit_units",
            "semester",
            "academic_session",
            "total_marks",
            "grade",
            "grade_point",
            "remarks",
            "is_released",
            "released_at",
            "created_at",
            "updated_at",
        )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def validate_coursework_marks(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Coursework marks cannot be negative."
            )

        if value > 40:
            raise serializers.ValidationError(
                "Coursework marks cannot be greater than 40."
            )

        return value

    def validate_exam_marks(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Exam marks cannot be negative."
            )

        if value > 60:
            raise serializers.ValidationError(
                "Exam marks cannot be greater than 60."
            )

        return value