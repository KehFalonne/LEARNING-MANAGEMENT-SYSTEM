from rest_framework import serializers
from django.utils import timezone
from courses.models import CourseOffering

from .models import (
    Assignment,
    AssignmentSubmission,
)


class LecturerAssignmentSerializer(
    serializers.ModelSerializer
):

    course_code = serializers.CharField(
        source="course_offering.course.code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="course_offering.course.title",
        read_only=True,
    )

    lecturer_name = serializers.SerializerMethodField()

    class Meta:
        model = Assignment

        fields = (
            "id",
            "course_offering",
            "course_code",
            "course_title",
            "lecturer",
            "lecturer_name",
            "title",
            "instructions",
            "attachment",
            "total_marks",
            "due_date",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "lecturer",
            "lecturer_name",
            "created_at",
            "updated_at",
        )

    def get_lecturer_name(self, obj):
        return obj.lecturer.user.get_full_name()

    def validate_course_offering(self, value):

        request = self.context["request"]

        if request.user.role != "LECTURER":
            raise serializers.ValidationError(
                "Only lecturers can create assignments."
            )

        try:
            lecturer = request.user.lecturer_profile

        except Exception:
            raise serializers.ValidationError(
                "Lecturer profile not found."
            )

        is_assigned = (
            value.teaching_assignments
            .filter(
                lecturer=lecturer,
            )
            .exists()
        )

        if not is_assigned:
            raise serializers.ValidationError(
                "You are not assigned to this course."
            )

        return value

    def create(self, validated_data):

        lecturer = (
            self.context["request"]
            .user
            .lecturer_profile
        )

        validated_data["lecturer"] = lecturer

        return super().create(validated_data)


class StudentAssignmentSerializer(
    serializers.ModelSerializer
):

    course_code = serializers.CharField(
        source="course_offering.course.code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="course_offering.course.title",
        read_only=True,
    )

    semester = serializers.CharField(
        source="course_offering.semester.name",
        read_only=True,
    )

    submitted = serializers.SerializerMethodField()

    submission_status = serializers.SerializerMethodField()

    marks = serializers.SerializerMethodField()

    feedback = serializers.SerializerMethodField()

    class Meta:
        model = Assignment

        fields = (
            "id",
            "course_offering",
            "course_code",
            "course_title",
            "semester",
            "title",
            "instructions",
            "attachment",
            "total_marks",
            "due_date",
            "status",
            "submitted",
            "submission_status",
            "marks",
            "feedback",
            "created_at",
        )

    def get_submission(self, obj):
        return getattr(
            obj,
            "student_submission",
            None,
        )

    def get_submitted(self, obj):
        return self.get_submission(obj) is not None

    def get_submission_status(self, obj):
        submission = self.get_submission(obj)

        if submission:
            return submission.status

        return None

    def get_marks(self, obj):
        submission = self.get_submission(obj)

        if submission:
            return submission.marks

        return None

    def get_feedback(self, obj):
        submission = self.get_submission(obj)

        if submission:
            return submission.feedback

        return None


class AssignmentSubmissionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AssignmentSubmission

        fields = (
            "id",
            "assignment",
            "file",
            "submitted_at",
            "status",
            "marks",
            "feedback",
            "graded_at",
        )

        read_only_fields = (
            "id",
            "assignment",
            "submitted_at",
            "status",
            "marks",
            "feedback",
            "graded_at",
        )


class StudentAssignmentSubmitSerializer(
    serializers.Serializer
):

    file = serializers.FileField()

    def validate_file(self, value):

        allowed_extensions = (
            ".pdf",
            ".doc",
            ".docx",
            ".zip",
        )

        filename = value.name.lower()

        if not filename.endswith(
            allowed_extensions
        ):
            raise serializers.ValidationError(
                "Only PDF, DOC, DOCX and ZIP files "
                "are allowed."
            )

        return value

    def save(self, **kwargs):

        student = self.context["student"]

        assignment = self.context["assignment"]

        uploaded_file = self.validated_data["file"]

        submission, created = (
            AssignmentSubmission.objects.update_or_create(
                assignment=assignment,
                student=student,
                defaults={
                    "file": uploaded_file,
                    "status": (
                        AssignmentSubmission
                        .SubmissionStatus
                        .SUBMITTED
                    ),
                },
            )
        )

        if timezone.now() > assignment.due_date:

            submission.status = (
                AssignmentSubmission
                .SubmissionStatus
                .LATE
            )

            submission.save()

        return submission