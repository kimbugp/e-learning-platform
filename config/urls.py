from django.contrib import admin
from django.urls import include, path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('app.authentication.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('courses/', include('app.courses.urls')),

]
