from django.shortcuts import get_object_or_404
from django.utils import timezone
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
                is_released=True,
            )
            .select_related(
                "student__user",
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .order_by(
                "course_offering__academic_session",
                "course_offering__semester",
                "course_offering__course__code",
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



class ReleaseGradeView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, grade_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can release "
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

        grade = get_object_or_404(
            Grade.objects.select_related(
                "course_offering",
            ),
            id=grade_id,
        )

        is_assigned = (
            grade.course_offering
            .teaching_assignments
            .filter(
                lecturer=lecturer,
            )
            .exists()
        )

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

        if grade.is_released:
            return Response(
                {
                    "detail": (
                        "This result is already released."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        grade.is_released = True
        grade.released_at = timezone.now()

        grade.save(
            update_fields=[
                "is_released",
                "released_at",
                "updated_at",
            ]
        )

        return Response(
            GradeSerializer(grade).data,
            status=status.HTTP_200_OK,
        )



#This is the Student list View that will used by the api
class StudentGradeListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "STUDENT":
            return Response(
                {
                    "detail": (
                        "Only students can access "
                        "their results."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            student = request.user.student_profile

        except Exception:
            return Response(
                {
                    "detail": "Student profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        grades = (
            Grade.objects
            .filter(
                student=student,
            )
            .select_related(
                "course_offering__course",
                "course_offering__semester",
                "course_offering__academic_session",
            )
            .order_by(
                "course_offering__academic_session",
                "course_offering__semester",
                "course_offering__course__code",
            )
        )

        serializer = GradeSerializer(
            grades,
            many=True,
        )

        return Response(serializer.data)


class ReleaseGradeView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, grade_id):

        if request.user.role != "LECTURER":
            return Response(
                {
                    "detail": (
                        "Only lecturers can release "
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

        grade = get_object_or_404(
            Grade.objects.select_related(
                "course_offering",
            ),
            id=grade_id,
        )

        is_assigned = (
            grade.course_offering
            .teaching_assignments
            .filter(
                lecturer=lecturer,
            )
            .exists()
        )

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

        if grade.is_released:
            return Response(
                {
                    "detail": "This result is already released."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        grade.is_released = True
        grade.released_at = timezone.now()
        grade.save(
            update_fields=[
                "is_released",
                "released_at",
                "updated_at",
            ]
        )

        return Response(
            GradeSerializer(grade).data,
            status=status.HTTP_200_OK,
        )