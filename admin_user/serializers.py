from rest_framework import serializers
from accounts.serializers import CustomUserSerializer
from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = ['id', 'activity_type', 'details', 'created_at']