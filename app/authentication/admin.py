from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.authentication.forms import UserCreation, UserUpdate
from app.authentication.models import User

from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserCreation
    form = UserUpdate
    model = User
    list_display = ['email', 'username','password' ]


admin.site.register(User, CustomUserAdmin)
