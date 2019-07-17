from django.urls import path

from . import views

urlpatterns = [
    path('create/',
         views.CourseCreateView .as_view(),
         name='course_create'),
    path('',
         views.CoursesListView.as_view(),
         name='courses_list'),
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),
    path('<pk>/delete/', views.CourseDeleteView.as_view(),
         name='course_delete'),
]
