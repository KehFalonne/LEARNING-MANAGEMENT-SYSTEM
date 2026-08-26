from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from enrollment.models import Enrollment

from .models import CourseOffering
from .serializers import CourseDetailSerializer


class StudentCourseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, offering_id):

        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": (
                        "Only students can access "
                        "student course pages."
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

        enrollment = get_object_or_404(
            Enrollment.objects.select_related(
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            ).prefetch_related(
                "course_offering__teaching_assignments__lecturer__user",
            ),
            student=student,
            course_offering_id=offering_id,
            status=Enrollment.Status.ACTIVE,
        )

        serializer = CourseDetailSerializer(
            enrollment.course_offering
        )

        return Response(serializer.data)