
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