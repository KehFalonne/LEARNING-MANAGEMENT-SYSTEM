from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import CourseOffering
from enrollment.models import Enrollment

from .models import Grade
from .serializers import GradeSerializer


class LecturerGradeListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, offering_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can access "
                        "course grades."
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

        course_offering = get_object_or_404(
            CourseOffering.objects.select_related(
                "course",
                "semester",
                "academic_session",
            ),
            id=offering_id,
        )

        is_assigned = course_offering.teaching_assignments.filter(
            lecturer=lecturer,
        ).exists()

        if not is_assigned:
            return Response(
                {
                    "detail": (
                        "You are not assigned to "
                        "this course."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        grades = (
            Grade.objects
            .filter(
                course_offering=course_offering,
            )
            .select_related(
                "student__user",
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .order_by(
                "student__student_id",
            )
        )

        serializer = GradeSerializer(
            grades,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, offering_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can enter "
                        "grades."
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

        course_offering = get_object_or_404(
            CourseOffering,
            id=offering_id,
        )

        is_assigned = course_offering.teaching_assignments.filter(
            lecturer=lecturer,
        ).exists()

        if not is_assigned:
            return Response(
                {
                    "detail": (
                        "You are not assigned to "
                        "this course."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        student_id = request.data.get(
            "student"
        )

        if not student_id:
            return Response(
                {
                    "detail": "Student is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_enrolled = Enrollment.objects.filter(
            student_id=student_id,
            course_offering=course_offering,
            status=Enrollment.Status.ACTIVE,
        ).exists()

        if not is_enrolled:
            return Response(
                {
                    "detail": (
                        "This student is not "
                        "actively enrolled in "
                        "this course."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        grade, created = Grade.objects.get_or_create(
            student_id=student_id,
            course_offering=course_offering,
        )

        serializer = GradeSerializer(
            grade,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        grade = serializer.save()

        return Response(
            GradeSerializer(grade).data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )