from django.urls import path

from .views import (
    LecturerAssignmentListCreateView,
    StudentAssignmentListView,
    StudentAssignmentSubmitView,
    LecturerAssignmentSubmissionListView,
    GradeAssignmentSubmissionView,
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

    path(
        "lecturer/<int:assignment_id>/submissions/",
        LecturerAssignmentSubmissionListView.as_view(),
        name="lecturer-assignment-submissions",
    ),

    path(
        "lecturer/submissions/<int:submission_id>/grade/",
        GradeAssignmentSubmissionView.as_view(),
        name="grade-assignment-submission",
    ),

]