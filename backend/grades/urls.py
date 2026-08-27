from django.urls import path

from .views import (
    LecturerGradeListCreateView,
    StudentGradeListView,
    ReleaseGradeView,
)


urlpatterns = [

    path(
        "lecturer/<int:offering_id>/",
        LecturerGradeListCreateView.as_view(),
        name="lecturer-grade-list-create",
    ),

    path(
        "student/",
        StudentGradeListView.as_view(),
        name="student-grade-list",
    ),
    
    path(
        "lecturer/<int:grade_id>/release/",
        ReleaseGradeView.as_view(),
        name="release-grade",
),

]