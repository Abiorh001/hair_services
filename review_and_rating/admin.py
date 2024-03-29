from django.contrib import admin
from .models import ReviewAndRating


class ReviewAndRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_provider', 'service', 'rating', 'review_text', 'review_date', 'id')
    search_fields = ('user', 'service_provider', 'service', 'rating', 'review_text', 'review_date')
    ordering = ('user', 'service_provider', 'service', 'rating', 'review_text', 'review_date')
    list_filter = ('user', 'service_provider', 'service', 'rating', 'review_text', 'review_date')


admin.site.register(ReviewAndRating, ReviewAndRatingAdmin)


