from django.apps import apps
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, TemplateView, View

from app import students
from app.courses.models import Rating

from ..models import Content, Course, Module


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = "content_form.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, exclude=["owner", "order", "created", "updated"]
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect(
                "module_content_list",
                pk=self.module.course.id,
                module_id=module_id,
            )
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(TemplateResponseMixin, View):
    def post(self, request, id, module_id=None, *args, **kwargs):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect(
            "module_content_list", pk=module.course.id, module_id=module_id
        )


class RateCourseView(View):
    def post(self, request, id, *args, **kwargs):
        value = request.POST.get("points", 0)
        rating = Rating(request.user.id, id, value)
        course = get_object_or_404(Course, id=id)
        Rating.objects.create(user=request.user, course=course, value=value)
        return redirect(
            "module_content_list",
            pk=course.id,
            module_id=course.modules.first().id,
        )


class DashBoardView(TemplateView, TemplateResponseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.filter(students__id=self.request.user.id)
        context["courses"] = courses
        return context
