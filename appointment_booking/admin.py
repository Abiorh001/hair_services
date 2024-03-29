from django.contrib import admin
from .models import Appointment, AppointmentCheckout


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_provider', 'service', 'date', 'time', 'status', 'notes', 'id')
    search_fields = ('user', 'service_provider', 'service', 'date', 'time', 'status', 'notes')
    ordering = ('user', 'service_provider', 'service', 'date', 'time', 'status', 'notes')
    list_filter = ('user', 'service_provider', 'service', 'date', 'time', 'status', 'notes')


admin.site.register(Appointment, AppointmentAdmin)


class AppointmentCheckoutAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'total_price', 'payment_status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('appointment', 'total_price', 'payment_status', 'payment_method', 'created_at', 'updated_at')
    ordering = ('appointment', 'total_price', 'payment_status', 'payment_method', 'created_at', 'updated_at')
    list_filter = ('appointment', 'total_price', 'payment_status', 'payment_method', 'created_at', 'updated_at')


admin.site.register(AppointmentCheckout, AppointmentCheckoutAdmin)
