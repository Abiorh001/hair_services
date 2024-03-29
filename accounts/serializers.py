from rest_framework import serializers
from .models import CustomUser, UserProfile
from django.core.exceptions import ValidationError
import re


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    two_factor_auth_token = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'phone_number', 'username', 'user_type', 'first_name', 'last_name', 'two_factor_auth_token', 'referral_code']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'user_type': {'required': True },
            
        }

    def validate_user_type(self, value):
        if value not in ["client", "professional", "admin"]:
            raise serializers.ValidationError("Invalid user type. User type must be client, professional, or admin.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
        }

        
class GetCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email',
                  'phone_number',
                  'username',
                  'first_name', 'last_name',
                  ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_picture = data.get('profile_picture')
        if profile_picture is not None:
            data['profile_picture'] = profile_picture.split('?')[0]
        return data
    

class GetUserProfileSerializer(serializers.ModelSerializer):
    user = GetCustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_picture = data.get('profile_picture')
        if profile_picture is not None:
            data['profile_picture'] = profile_picture.split('?')[0]
        return data
    

class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    class Meta:
        model = CustomUser
        fields = ['password']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    class Meta:
        model = CustomUser
        fields = ['password']

    