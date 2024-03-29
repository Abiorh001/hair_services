from django.contrib import admin
from .models import Service
from service_categories.models import ServiceCategory


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')
    list_filter = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ServiceCategory, ServiceCategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'service_category', 'service_name', 'price', 'duration_minutes', 'created_at', 'updated_at')
    list_filter = ('service_provider', 'service_category', 'service_name', 'price', 'duration_minutes', )
    search_fields = ('service_provider', 'service_category', 'service_name', 'price', 'duration_minutes',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Service, ServiceAdmin)
