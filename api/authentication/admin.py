from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.authentication.forms import UserCreation, UserUpdate
from api.authentication.models import User

from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserCreation
    form = UserUpdate
    model = User
    list_display = ['email', 'username','password' ]


admin.site.register(User, CustomUserAdmin)
