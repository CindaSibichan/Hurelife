from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DoctorAvailability)
admin.site.register(Appointment)
admin.site.register(Payments)
admin.site.register(SetOfflineChat)
admin.site.register(Prescription)
admin.site.register(DoctorStatus)