from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from app.authentication.models import User


class UserCreation(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "username",
            "email",
            "is_student",
            "is_teacher",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["username"].help_text = None
        self.fields["password2"].help_text = None
        self.fields["password2"].label = "Confirm"

    def save(self, commit=True):
        user = super().save(commit)
        if user.is_teacher:
            self.add_group(user, "teacher")
        return user

    def add_group(self, user, group):
        my_group, _ = Group.objects.get_or_create(name=group)
        my_group.user_set.add(user)


class UserUpdate(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ("username", "email")
