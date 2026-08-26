from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StudentDashboardSerializer


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

        serializer = StudentDashboardSerializer(student)

        return Response(serializer.data)