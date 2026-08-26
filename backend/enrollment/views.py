from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StudentDashboardSerializer

from enrollment.serializers import StudentEnrollmentSerializer


class StudentDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": "Only students can access this endpoint."
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

        student_serializer = StudentDashboardSerializer(student)

        enrollments = (
            student.enrollments
            .select_related(
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .filter(status="ACTIVE")
        )

        enrollment_serializer = StudentEnrollmentSerializer(
            enrollments,
            many=True,
        )

        return Response(
            {
                "student": student_serializer.data,
                "courses": enrollment_serializer.data,
            }
        )