# authentication/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'is_active']  # Removido is_staff e is_superuser
    search_fields = ['email', 'name']
    ordering = ['email']
    list_filter = []  

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'address', 'phone')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Remova filter_horizontal, pois groups e user_permissions não são campos do modelo User
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
