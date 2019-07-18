from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from ..models import Course


class CourseOwnerMixin(LoginRequiredMixin):
    model = Course

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseModelEditMixin(CourseOwnerMixin):
    template_name = 'course_create.html'
    success_url = reverse_lazy('courses_list')
    fields = ['subject', 'title', 'slug', 'overview']


class CourseCreateView(CourseModelEditMixin, PermissionRequiredMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, CourseModelEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, CourseOwnerMixin,
                       DeleteView):
    template_name = 'course_delete.html'
    success_url = reverse_lazy('courses_list')
    permission_required = 'courses.delete_course'


class CoursesListView(CourseOwnerMixin, ListView):
    template_name = 'courses_list.html'
