from django.urls import path

from .views import content_view, modules_view, courses_views

urlpatterns = [
    # students
    path('course/', courses_views.CourseListView.as_view(),
         name='student_courses_list'),
    path('course/subject/<slug:subject>)/',
         courses_views.CourseListView.as_view(),
         name='student_course_list_subject'),
    path('course/<slug:slug>/',
         courses_views.CourseDetailView.as_view(),
         name='student_course_detail'),

    # admin
    path('create/',
         courses_views.CourseCreateView.as_view(),
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
    path('<int:pk>/module/',
         modules_view.CourseModuleUpdateView.as_view(),
         name='course_module_update'),
    path('<int:pk>/module/<int:module_id>/',
         modules_view.ModuleContentListView.as_view(),
         name='module_content_list'),

    # content
    path('module/<int:module_id>/content/<model_name>/',
         content_view.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         content_view.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('module/<int:module_id>/content_view/<id>/',
         content_view.ContentDeleteView.as_view(),
         name='module_content_delete'),

]
