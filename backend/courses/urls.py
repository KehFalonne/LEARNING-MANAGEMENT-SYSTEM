from django.urls import path

from .views import StudentCourseDetailView


urlpatterns = [
    path(
        "student/<int:offering_id>/",
        StudentCourseDetailView.as_view(),
        name="student-course-detail",
    ),
]