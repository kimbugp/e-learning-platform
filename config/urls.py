from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app.courses.views.content_view import DashBoardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashBoardView.as_view(template_name='home.html'), name='home'),
    path('users/', include(('app.authentication.urls', 'user')),),
    path('users/', include('django.contrib.auth.urls')),
    path('courses/', include('app.courses.urls')),
    path('students/', include('app.students.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
