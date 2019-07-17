from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserCreation


class SignUpView(CreateView):
    form_class = UserCreation
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
