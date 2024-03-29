from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Referral

# Customize the UserAdmin class
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)  


class CustomUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',  'get_full_address', 'country')
    list_filter = ('country',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'country')
    ordering = ('-created_at',)

    # def get_date_of_birth(self, obj):
    #     return obj.date_of_birth.strftime('%Y-%m-%d')

    # get_date_of_birth.short_description = 'Date of Birth'

    def get_full_address(self, obj):
        return f'{obj.residential_address}, {obj.city}, {obj.state} {obj.postal_code}'

    get_full_address.short_description = 'Address'


admin.site.register(UserProfile, CustomUserProfileAdmin)


class CustomReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer_user', 'referred_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('referrer_user__username', 'referrer_user__email', 'referrer_user__first_name', 'referrer_user__last_name', 'referred_user__username', 'referred_user__email', 'referred_user__first_name', 'referred_user__last_name')
    ordering = ('-created_at',)


admin.site.register(Referral, CustomReferralAdmin)