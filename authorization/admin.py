from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Doctor)
# admin.site.register(Patient)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'is_verified', 'is_active')
    actions = ['approve_doctors']

    def approve_doctors(self, request, queryset):
        queryset.update(is_active=True)
    approve_doctors.short_description = "Approve selected doctors"


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname' ,'is_verified')    