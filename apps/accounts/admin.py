from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'is_locked', 'is_active', 'last_login']
    list_filter   = ['role', 'is_locked', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering      = ['username']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Forensic DB Role', {'fields': ('role', 'is_locked', 'must_change_password', 'login_attempts', 'last_login_ip')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Forensic DB Role', {'fields': ('role',)}),
    )
