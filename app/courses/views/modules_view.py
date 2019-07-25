from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View

from ..models import Course, Module
from ..forms import ModuleFormSet


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'modules.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'content_list.html'

    def get(self, request, pk, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user, course__id=pk)
        return self.render_to_response({'module': module})