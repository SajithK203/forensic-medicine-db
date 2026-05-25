from django.contrib import admin
from .models import Staff, Doctor


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display  = ['staff_id', 'full_name', 'staff_type', 'department', 'contact_no', 'is_active']
    list_filter   = ['staff_type', 'is_active']
    search_fields = ['staff_id', 'full_name', 'email']
    ordering      = ['full_name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ['doctor_id', 'full_name', 'jmo_type', 'nmc_number', 'specialization', 'is_active']
    list_filter   = ['jmo_type', 'is_active']
    search_fields = ['doctor_id', 'full_name', 'nmc_number']
    ordering      = ['full_name']
