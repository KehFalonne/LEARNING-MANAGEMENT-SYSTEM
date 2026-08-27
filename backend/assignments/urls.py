from django.urls import path

from .views import (
    LecturerAssignmentListCreateView,
    StudentAssignmentListView,
    StudentAssignmentSubmitView
)

urlpatterns = [

    path(
        "lecturer/",
        LecturerAssignmentListCreateView.as_view(),
        name="lecturer-assignment-list-create",
    ),

    path(
        "student/",
        StudentAssignmentListView.as_view(),
        name="student-assignment-list",
    ),

    path(
        "student/<int:assignment_id>/submit/",
        StudentAssignmentSubmitView.as_view(),
        name="student-assignment-submit",
    ),

]