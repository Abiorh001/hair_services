from django.contrib import admin
from .models import (
    ServiceProviderProfile,
    ServiceProviderAvailability,
)


class ServiceProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'business_description', 'business_address', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    list_filter = ('business_name', 'business_address', 'city', 'state', 'country')
    search_fields = ('business_name', 'business_address', 'city', 'state', 'country')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ServiceProviderProfile, ServiceProviderProfileAdmin)
                    

class ServiceProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'date', 'start_time', 'end_time', 'created_at', 'updated_at')
    list_filter = ('service_provider', 'date', 'start_time', 'end_time',)
    search_fields = ('service_provider', 'date', 'start_time', 'end_time',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ServiceProviderAvailability, ServiceProviderAvailabilityAdmin)
