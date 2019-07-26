from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from app.authentication.models import User


class UserCreation(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'is_student',
                  'is_teacher', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirm"


class UserUpdate(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'email')
