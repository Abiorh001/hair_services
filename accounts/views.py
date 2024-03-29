from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.request import Request
from .models import CustomUser, UserProfile, Referral
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.tasks.email_verification import send_verification_email
from accounts.tasks.login_notification import send_login_notification_email
from accounts.tasks.forget_password import send_forget_password_email
from accounts.tasks.two_factor_auth_token import resend_two_factor_auth_token
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import check_password, make_password
import requests
from datetime import datetime
from decouple import config
import os
from hair_services.settings import BASE_DIR
from fcm_django.models import FCMDevice
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import secrets
from django.urls import reverse


# generate referral code
def generate_referral_code():
    return secrets.token_hex(6)



# generate otp
def generate_two_factor_auth_token():
    import random
    return random.randint(100000, 999999)


# get user location information
def get_location_info(self, ip_address):
    # Use an external API to get location information
    api_key = config('IPSTACK_API_KEY')
    url = f"http://api.ipstack.com/{ip_address}?access_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        location_data = response.json()
        user_location = f"{location_data['city']}, {location_data['region_name']}, {location_data['country_name']}"
        return user_location
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        print(f"Error fetching location information: {e}")
        return None


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Registration of a new user requires the following fields:",
        tags=['User Management'],
        request_body=CustomUserSerializer,
        responses={201: CustomUserSerializer(many=False)}
    )
    def post(self, request: Request) -> Response:
        data = request.data
        password = data.get('password')
        two_factor_auth_token = generate_two_factor_auth_token()
        data["two_factor_auth_token"] = two_factor_auth_token
        serializer = CustomUserSerializer(data=data)
        email = data.get('email')
        data["referral_code"] = generate_referral_code()
        refer_code = request.query_params.get('referral_code')
        if serializer.is_valid():
            serializer.save()
            new_user = CustomUser.objects.get(email=email)
            new_user.user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
            if new_user.user_ip_address is None:
                new_user.user_ip_address = request.META.get('REMOTE_ADDR')
            new_user.save()
            # get the existing user referral code from the query params
            if refer_code:
                existing_user = CustomUser.objects.filter(referral_code=refer_code).first()
                if existing_user:
                    # create a new referral instance
                    referral = Referral.objects.create(
                        referrer_user=existing_user,
                        referred_user=new_user
                        )
                    referral.save()
                else:
                    pass
        
            # send email to user to notify them of their two factor authentication token
            send_verification_email.delay(email, two_factor_auth_token)

            response = {
                "status": "success",
                "message": "Account created successfully,please check your email for your two factor authentication token",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_response = {
            "status": "error",
            "message": "User not registered",
            "data": serializer.errors,
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class ResendTwoFactorAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Resend two factor auth token",
        operation_description="Resend two factor auth token to user email",
        tags=['User Management'],
        manual_parameters=[
            openapi.Parameter(
                name='email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='User email',
                required=True,
            ),
        ],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Two Factor auth token resent successfully or Email is required or User not found or Account already verified'),
            }
        )}
    )
    def get(self, request):
        email = request.query_params.get('email')

        if email is None:
            return Response({"status": "error", "message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)

            if user.two_factor_complete:
                return Response({"status": "error", "message": "Account already verified"}, status=status.HTTP_400_BAD_REQUEST)

            token = generate_two_factor_auth_token()
            resend_two_factor_auth_token.delay(email=email, token=token)
            user.two_factor_auth_token = token
            user.save()

            return Response({"status": "success", "message": "Two Factor auth token resent successfully"}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyTwoFactorAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="New User verify account",
        operation_description="Verify account of new user with user email and two factor authentication token sent to user email",
        tags=['User Management'],
        manual_parameters=[
            openapi.Parameter(
                name='email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='User email',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'two_factor_auth_token': openapi.Schema(type=openapi.TYPE_STRING, description='Two factor authentication token'),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='account verified successfully or invalid token'),
            }
        )}
    )
    def patch(self, request: Request):
        
        email = request.query_params.get('email')
        if email is None:
            bad_response = {
                    "status": "error",
                    "message": "Email is required",
                }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        two_factor_auth_token = request.data.get('two_factor_auth_token')
        try:
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                bad_response = {
                    "status": "error",
                    "message": "User not found",
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
            if user.two_factor_complete is True:
                bad_response = {
                    "status": "error",
                    "message": "Account already verified",
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        
            if user.two_factor_auth_token == two_factor_auth_token:
                # check if token has expired
                time_difference = timezone.now() - user.created_at
                minutes_difference = time_difference.total_seconds() / 60

                new_time_difference = timezone.now() - user.updated_at
                new_minutes_difference = new_time_difference.total_seconds() / 60

                if user.created_at == user.updated_at and minutes_difference > 2:
                    response = {
                            "status": "error",
                            "message": "Token expired. Please request a new one.",
                        }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                elif user.created_at != user.updated_at and new_minutes_difference > 2:
                    response = {
                            "status": "error",
                            "message": "Token expired. Please request a new one.",
                        }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                user.two_factor_complete = True
                user.two_factor_auth_token = None
                user.save()
                response = {
                        "status": "success",
                        "message": "Account verified successfully"
                    }
                return Response(response, status=status.HTTP_200_OK)
            bad_response = {
                    "status": "error",
                    "message": "Invalid token",
                }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            bad_response = {
                    "status": "error",
                    "message": "User not found",
                }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login an existing user",
        operation_description="Login of an existing user requires the following fields:",
        tags=['User Management'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Login successful or User not found with this email or Incorrect password'),
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                'user_profile': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Login successful or User not found with this email or Incorrect password'),
                        'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User id'),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='User username'),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                    }
                )
            }
        )}
    )
    def post(self, request: Request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user is None:
            bad_request_response = {
                    "status": "failed",
                    "message": "User not found with this email"
                }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)
        if existing_user.two_factor_complete is False:
            bad_request_response = {
                    "status": "failed",
                    "message": "account not verified, please verify your account"
                }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)
        if check_password(password, existing_user.password) is False:
            bad_request_response = {
                    "status": "failed",
                    "message": "Incorrect password"
                }
            return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)
        user_request_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_request_ip_address is None:
            user_request_ip_address = request.META.get('REMOTE_ADDR')
        ip_address = user_request_ip_address
        
        if existing_user.user_ip_address is None:
            existing_user.user_ip_address = ip_address
            existing_user.save()

        if existing_user.user_ip_address != user_request_ip_address:
            
            # send email to user to notify them of login from a different location
            context = {
                    'user_first_name': existing_user.first_name,
                    'user_new_location': get_location_info(self, ip_address=ip_address),
                    'user_new_ip_address': ip_address,
                    'user_new_device': request.META.get('HTTP_USER_AGENT'),
                    'formatted_time': datetime.now().strftime("%A, %B %d, %Y at %I:%M%p"),
                    'change_password_link': f"https://api.hairsol.uk/api/v1/users/forget-password/?email={email}",
                }

            # Render the HTML content using the template
            template_path = os.path.join(BASE_DIR, 'utils', 'templates', 'accounts', 'login_notification_email.html')
            html_content = render_to_string(template_path, context, request=request)
            
            # Send the email to the user using Celery
            send_login_notification_email.delay(email, html_content)
        
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    if user:
                        user_profile_data = {
                            "status": "success",
                            "message": "Login successful",
                            "user_id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "username": user.username,
                            "phone_number": user.phone_number,
                            "user_type": user.user_type,
                            "user_verified": user.two_factor_complete,
                        }
                        response.data['user_profile'] = user_profile_data
                except CustomUser.DoesNotExist:
                    bad_request_response = {
                            "status": "failed",
                            "message": "User not found"
                        }
                    return Response(bad_request_response,
                                    status=status.HTTP_400_BAD_REQUEST)
        return response
            

class CreateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a newly registered user profile",
        operation_description="Creation of a newly registered user profile requires the following fields:",
        tags=['User Management'],
        request_body=UserProfileSerializer,
        responses={201: UserProfileSerializer(many=False)}
    )
    def post(self, request: Request):
        data = request.data
        user = request.user
        data["user"] = user.id 
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "User Profile created successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_response = {
            "status": "error",
            "message": "Profile not created",
            "data": serializer.errors,
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve user profile",
        operation_description="Retrieve user profile of logged in user",
        tags=['User Management'],
        responses={200: GetUserProfileSerializer(many=False)}
    )
    def get(self, request: Request):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
            serializer = GetUserProfileSerializer(user_profile)
            response = {
                "status": "success",
                "message": "User Profile retrieved successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User Profile not found",
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Update user profile of logged in user",
        tags=['User Management'],
        request_body=UserProfileSerializer,
        responses={200: GetUserProfileSerializer(many=False)}
    )
    def patch(self, request: Request):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "User Profile updated successfully",
                    "data": serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)
            bad_response = {
                "status": "error",
                "message": "User Profile not updated",
                "data": serializer.errors,
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User Profile not found",
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)


class UpdateUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update user account",
        operation_description="Update user account of logged in user",
        tags=['User Management'],
        request_body=CustomUserSerializer,
        responses={200: CustomUserSerializer(many=False)}
    )
    def patch(self, request: Request):
        user = request.user
        try:
            user = CustomUser.objects.get(id=user.id)
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "User Account updated successfully",
                    "data": serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)
            bad_response = {
                "status": "error",
                "message": "User Account not updated",
                "data": serializer.errors,
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User Account not found",
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)


class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Change user password",
        operation_description="Change user password of logged in user",
        tags=['User Management'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old password'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='User password updated successfully or User password not updated'),
            }
        )}
    )
    def patch(self, request: Request):
        auth_user = request.user
        user = CustomUser.objects.get(id=auth_user.id)
        old_password = request.data.get('old_password')
        password = request.data.get('password')
        if check_password(old_password, user.password) is False:
            bad_response = {
                "status": "error",
                "message": "Old password is incorrect",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        if old_password == password:
            bad_response = {
                "status": "error",
                "message": "New password must be different from the old password",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChangeUserPasswordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            user.set_password(password)
            user.save()
            response = {
                "status": "success",
                "message": "User password updated successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            bad_response = {
                "status": "error",
                "message": "User password not updated",
                "data": serializer.errors,
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
                 

class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Forget user password",
        operation_description="Forget user password",
        tags=['User Management'],
        manual_parameters=[
            openapi.Parameter(
                name='email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='User email',
                required=True,
            ),
        ],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Reset password token sent successfully to your email or User not found'),
            }
        )}
    )
    def get(self, request: Request):
        
        try:
            email = request.query_params.get('email')
            user = CustomUser.objects.get(email=email)
            user.reset_password_token = generate_two_factor_auth_token()
            user.save()
            reset_token = user.reset_password_token
            send_forget_password_email.delay(email, reset_token)
            response = {
                "status": "success",
                "message": "Reset password token sent successfully to your email",
            }
            return Response(response, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User not found",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Reset user password",
        operation_summary="Reset user password",
        tags=['User Management'],
        manual_parameters=[
            openapi.Parameter(
                name='email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='User email',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reset_password_token': openapi.Schema(type=openapi.TYPE_STRING, description='Reset password token'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Password reset successfully or Reset password token has not been generated for this user or Invalid token or User not found'),
            }
        )}
    )
    def patch(self, request: Request):
        email = request.query_params.get('email')
        reset_password_token = request.data.get('reset_password_token')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            if user.reset_password_token is None:
                bad_response = {
                    "status": "error",
                    "message": "Reset password token has not been generated for this user",
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
            if user.reset_password_token != reset_password_token:
                bad_response = {
                    "status": "error",
                    "message": "Invalid token",
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
            serializer = ResetPasswordSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                password = serializer.validated_data.get('password')
                if check_password(password, user.password):
                    bad_response = {
                        "status": "error",
                        "message": "New password must be different from the old password",
                    }
                    return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
                if user.reset_password_token == reset_password_token:
                    user.reset_password_token = None
                    user.set_password(password)
                    user.save()
                    response = {
                        "status": "success",
                        "message": "Password reset successfully",
                    }
                    return Response(response, status=status.HTTP_200_OK)
            else:
                bad_response = {
                    "status": "error",
                    "message": "Password not reset",
                    "data": serializer.errors,
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User not found",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete user account",
        operation_description="Delete user account of logged in user",
        tags=['User Management'],
        responses={204: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='User Account deleted successfully or User Account not found'),
            }
        )}
    )
    def delete(self, request: Request):
        user = request.user
        try:
            user = CustomUser.objects.get(id=user.id)
            user.delete()
            response = {
                "status": "success",
                "message": "User Account deleted successfully",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User Account not found",
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)
    

class ReferralNewUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Referral new user",
        operation_description="Referral new user",
        tags=['User Management'],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Referral successful or User not found'),
            }
        )}
    )
    def get(self, request: Request):
        user = request.user
        try:
            user = CustomUser.objects.get(id=user.id)
            user_referral_code = user.referral_code
            sign_up_url = request.build_absolute_uri(reverse('register')) + f"?referral_code={user_referral_code}"
            response = {
                "status": "success",
                "message": "Referral link retrieved successful",
                "referral_sign_up_url": sign_up_url,
            }
            return Response(response, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            bad_response = {
                "status": "error",
                "message": "User not found",
            }
            return Response(bad_response, status=status.HTTP_404_NOT_FOUND)

class RegisterFcmDevice(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Register FCM device",
        operation_description="Register FCM device of logged in user",
        tags=['User Management'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'registration_id': openapi.Schema(type=openapi.TYPE_STRING, description='Registration id'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type'),
            }
        ),
        responses={201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='success or error'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='FCM device registered successfully or FCM device not registered'),
            }
        )}
    )
    def post(self, request: Request):
        user = request.user
        data = request.data
        data["user"] = user.id
        fcm_token = data.get('token')
        existing_user = CustomUser.objects.filter(id=user.id).first()
        existing_device = FCMDevice.objects.filter(user=user, registration_id=fcm_token).first()
        if not existing_device:
            # If the device is not registered, create an FCMDevice instance
            device = FCMDevice.objects.create(
                user=user,
                registration_id=fcm_token,
                type="web",
                name=existing_user.first_name
            )
            device.save()
            response = {
                "status": "success",
                "message": "FCM device registered successfully",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_response = {
            "status": "error",
            "message": "FCM device not registered",
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        # serializer = FcmDeviceSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     response = {
        #         "status": "success",
        #         "message": "FCM device registered successfully",
        #         "data": serializer.data,
        #     }
        #     return Response(response, status=status.HTTP_201_CREATED)
        # bad_response = {
        #     "status": "error",
        #     "message": "FCM device not registered",
        #     "data": serializer.errors,
        # }
        # return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)