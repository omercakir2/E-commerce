from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['email', 'gender', 'is_staff']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'gender','profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'gender', 'is_staff', 'is_superuser',)}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
