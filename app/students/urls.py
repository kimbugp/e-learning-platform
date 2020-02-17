from django.urls import path
from . import views

urlpatterns = [
    path(
        "enroll/",
        views.StudentEnrollCourseView.as_view(),
        name="student_enroll",
    )
]
