from django.urls import path

from . import courses_views
from . import modules_view
from . import content_view

urlpatterns = [

     ## courses
    path('create/',
         courses_views.CourseCreateView .as_view(),
         name='course_create'),
    path('',
         courses_views.CoursesListView.as_view(),
         name='courses_list'),
    path('<pk>/edit/',
         courses_views.CourseUpdateView.as_view(),
         name='course_edit'),
    path('<pk>/delete/', courses_views.CourseDeleteView.as_view(),
         name='course_delete'),

     #  modules
    path('<pk>/module/',
         modules_view.CourseModuleView.as_view(),
         name='course_module'),

     ## content
    path('module/<int:module_id>/content/<model_name>/create/',
         content_view.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         content_view.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
]
