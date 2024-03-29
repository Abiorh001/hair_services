from rest_framework import serializers
from .models import ReviewAndRating
from accounts.serializers import CustomUserSerializer
from services.serializers import ServiceSerializer, GetServiceSerializer
from professional_service_provider.serializers import ServiceProviderProfileSerializer


class ReviewServiceSerializer(serializers.ModelSerializer):
    
    service = GetServiceSerializer(read_only=True)

    class Meta:
        model = ReviewAndRating
        fields = ['id', 'service', 'review_text', 'review_date',]


class RatingReviewServiceSerializer(serializers.ModelSerializer):
    
    service = GetServiceSerializer(read_only=True)

    class Meta:
        model = ReviewAndRating
        fields = ['id', 'service_provider', 'service', 'review_text', 'rating', 'review_date',]