from django.urls import path

from .views import SignUpView, ResetPassword

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('change_password/', ResetPassword.as_view(), name='change_password'),
]
