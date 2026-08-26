from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from enrollment.models import Enrollment

from courses.models import CourseOffering
from courses.serializers import CourseDetailSerializer


class StudentDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": "Only students can access the student dashboard."
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

        enrollments = (
            Enrollment.objects
            .filter(
                student=student,
                status=Enrollment.Status.ACTIVE,
            )
            .select_related(
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .order_by(
                "course_offering__course__code"
            )
        )

        courses = []

        for enrollment in enrollments:

            offering = enrollment.course_offering

            courses.append(
                {
                    "id": offering.id,
                    "course_code": offering.course.code,
                    "course_title": offering.course.title,
                    "credit_units": offering.course.credit_units,
                    "semester": offering.semester.name,
                    "academic_session": offering.academic_session.name,
                    "status": enrollment.status,
                }
            )

        return Response(
            {
                "student": {
                    "full_name": student.user.get_full_name(),
                    "student_id": student.student_id,
                    "programme_name": student.programme.name,
                    "level_name": student.level.name,
                    "status": student.status,
                },
                "courses": courses,
            }
        )


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