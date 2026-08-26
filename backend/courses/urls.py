from django.urls import path

from .views import (
    StudentCourseDetailView,
    StudentLearningMaterialsView,
    )


urlpatterns = [
    path(
        "student/<int:offering_id>/",
        StudentCourseDetailView.as_view(),
        name="student-course-detail",
    ),
    path(
    "student/<int:offering_id>/materials/",
    StudentLearningMaterialsView.as_view(),
    name="student-learning-materials",
),
]