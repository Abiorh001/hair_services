from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/register/', views.RegistrationView.as_view(), name='register'),
    path('users/verify-account/', views.VerifyTwoFactorAuthTokenView.as_view(),
         name='verify-account'),
    path('users/resend-verification-code/', views.ResendTwoFactorAuthTokenView.as_view(),
         name='resend-verification-code'),
     
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register-profile/', views.CreateUserProfileView.as_view(),
         name='user-profile'),
    path('users/profile/', views.RetrieveUpdateUserProfileView.as_view(),
         name='retrieve-update-user-profile'),
    path('users/update-account/', views.UpdateUserAccountView.as_view(), name='update-user-account'),
    path('users/change-password/', views.ChangeUserPasswordView.as_view(), name='change-password'),
    path('users/forget-password/', views.ForgetPasswordView.as_view(), name='forgot-password'),
    path('users/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('users/delete-account/', views.DeleteUserAccountView.as_view(), name='delete-account'),
    path('users/referral-new-user/', views.ReferralNewUserView.as_view(), name='referral-new-user'),
    path('users/push-notification/', views.RegisterFcmDevice.as_view(), name='push-notification'),  
]