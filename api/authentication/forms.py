from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from api.authentication.models import User


class UserCreation(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class UserUpdate(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'email')
