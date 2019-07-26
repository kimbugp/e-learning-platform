from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import reverse_lazy
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from app.students.forms import CourseEnrollForm

from ..models import Course, Subject


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
    fields = ['subject', 'title', 'overview', 'image']

    def model_form_upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {
            'form': form
        })


class CourseCreateView(CourseModelEditMixin, PermissionRequiredMixin,
                       CreateView):
    permission_required = 'courses.create_course'


class CourseUpdateView(PermissionRequiredMixin, CourseModelEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, CourseOwnerMixin,
                       DeleteView):
    template_name = 'course_delete.html'
    success_url = reverse_lazy('courses_list')
    permission_required = 'courses.delete_course'


class CoursesListView(CourseOwnerMixin, ListView):
    template_name = 'courses_list.html'


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules')).filter(total_modules__gt=0)
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects, 'subject': subject, 'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_enrolled = False
        if self.object.students.all().filter(id=self.request.user.id):
            is_enrolled = True

        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        context['is_enrolled'] = is_enrolled
        return context
