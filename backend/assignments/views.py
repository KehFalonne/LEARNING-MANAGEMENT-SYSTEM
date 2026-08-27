
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from enrollment.models import Enrollment
from .models import Assignment, AssignmentSubmission
from .serializers import LecturerAssignmentSerializer
from django.utils import timezone
from rest_framework import status

from .models import(
    Assignment,
    AssignmentSubmission,
)
from .serializers import (
    LecturerAssignmentSerializer,
    StudentAssignmentSerializer,
    AssignmentSubmissionSerializer,
    StudentAssignmentSubmitSerializer,
    LecturerSubmissionSerializer,
    GradeAssignmentSubmissionSerializer,
)

class LecturerAssignmentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can access "
                        "this endpoint."
                    )
                },
                status=403,
            )

        try:
            lecturer = request.user.lecturer_profile

        except Exception:
            return Response(
                {
                    "detail": "Lecturer profile not found."
                },
                status=404,
            )

        assignments = (
            Assignment.objects
            .filter(
                lecturer=lecturer,
            )
            .select_related(
                "course_offering__course",
                "lecturer__user",
            )
            .order_by(
                "-created_at",
            )
        )

        serializer = LecturerAssignmentSerializer(
            assignments,
            many=True,
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = LecturerAssignmentSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        assignment = serializer.save()

        return Response(
            LecturerAssignmentSerializer(
                assignment,
                context={
                    "request": request,
                },
            ).data,
            status=201,
        )

class StudentAssignmentListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": (
                        "Only students can access "
                        "this endpoint."
                    )
                },
                status=403,
            )

        try:
            student = request.user.student_profile

        except Exception:
            return Response(
                {
                    "detail": "Student profile not found."
                },
                status=404,
            )

        active_offerings = Enrollment.objects.filter(
            student=student,
            status=Enrollment.Status.ACTIVE,
        ).values_list(
            "course_offering_id",
            flat=True,
        )

        assignments = (
            Assignment.objects
            .filter(
                course_offering_id__in=active_offerings,
                status=Assignment.Status.PUBLISHED,
            )
            .select_related(
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .prefetch_related(
                Prefetch(
                    "submissions",
                    queryset=AssignmentSubmission.objects.filter(
                        student=student,
                    ),
                    to_attr="student_submission_list",
                )
            )
            .order_by("due_date")
        )

        # Attach one submission directly to each assignment
        for assignment in assignments:

            submissions = getattr(
                assignment,
                "student_submission_list",
                [],
            )

            assignment.student_submission = (
                submissions[0]
                if submissions
                else None
            )

        serializer = StudentAssignmentSerializer(
            assignments,
            many=True,
        )

        return Response(serializer.data)


class StudentAssignmentSubmitView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, assignment_id):

        # Only students can submit
        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": (
                        "Only students can submit "
                        "assignments."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get student profile
        try:
            student = request.user.student_profile

        except Exception:
            return Response(
                {
                    "detail": "Student profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get assignment
        try:
            assignment = (
                Assignment.objects
                .select_related(
                    "course_offering",
                )
                .get(
                    id=assignment_id,
                )
            )

        except Assignment.DoesNotExist:
            return Response(
                {
                    "detail": "Assignment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Assignment must be published
        if assignment.status != Assignment.Status.PUBLISHED:
            return Response(
                {
                    "detail": (
                        "This assignment is not "
                        "available for submission."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check student enrollment
        is_enrolled = Enrollment.objects.filter(
            student=student,
            course_offering=assignment.course_offering,
            status=Enrollment.Status.ACTIVE,
        ).exists()

        if not is_enrolled:
            return Response(
                {
                    "detail": (
                        "You are not enrolled in "
                        "this course."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate uploaded file
        serializer = StudentAssignmentSubmitSerializer(
            data=request.data,
            context={
                "student": student,
                "assignment": assignment,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        submission = serializer.save()

        return Response(
            AssignmentSubmissionSerializer(
                submission,
                context={
                    "request": request,
                },
            ).data,
            status=status.HTTP_201_CREATED,
        )


class LecturerAssignmentSubmissionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, assignment_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can access "
                        "assignment submissions."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            lecturer = request.user.lecturer_profile

        except Exception:
            return Response(
                {
                    "detail": "Lecturer profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            assignment = (
                Assignment.objects
                .select_related(
                    "course_offering__course",
                    "lecturer__user",
                )
                .get(
                    id=assignment_id,
                    lecturer=lecturer,
                )
            )

        except Assignment.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Assignment not found or you do "
                        "not have permission to access it."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        submissions = (
            AssignmentSubmission.objects
            .filter(
                assignment=assignment,
            )
            .select_related(
                "student__user",
                "assignment__course_offering__course",
            )
            .order_by(
                "student__student_id",
            )
        )

        serializer = LecturerSubmissionSerializer(
            submissions,
            many=True,
        )

        return Response(
            {
                "assignment": {
                    "id": assignment.id,
                    "title": assignment.title,
                    "course_code": (
                        assignment
                        .course_offering
                        .course
                        .code
                    ),
                    "course_title": (
                        assignment
                        .course_offering
                        .course
                        .title
                    ),
                    "total_marks": assignment.total_marks,
                    "due_date": assignment.due_date,
                },
                "submissions": serializer.data,
            }
        )


class GradeAssignmentSubmissionView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, submission_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can grade "
                        "assignment submissions."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            lecturer = request.user.lecturer_profile

        except Exception:
            return Response(
                {
                    "detail": "Lecturer profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            submission = (
                AssignmentSubmission.objects
                .select_related(
                    "assignment__lecturer",
                    "assignment__course_offering__course",
                    "student__user",
                )
                .get(
                    id=submission_id,
                    assignment__lecturer=lecturer,
                )
            )

        except AssignmentSubmission.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Submission not found or you do "
                        "not have permission to grade it."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GradeAssignmentSubmissionSerializer(
            submission,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        submission = serializer.save()

        return Response(
            LecturerSubmissionSerializer(
                submission,
            ).data
        )