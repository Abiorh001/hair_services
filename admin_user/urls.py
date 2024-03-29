from django.urls import path
from .views import (
    AdminListAllUserView,
    AdminListAllClientView,
    AdminListAllProfessionalView,
    AdminListNewUserView,
    AdminListAllServiceProviderView,
    AdminListAllAppointmentView,
    AdminListAllNewBookedAppointmentView,
    AdminListAllCompletedAppointmentView,
    AdminListNewUserForTheWeek,
    RetrieveUpdateDeleteServiceProviderView,
    CreateServiceProviderView,
    UserActivityView,
)

urlpatterns = [
    path('hairsol-admin/all-users/', AdminListAllUserView.as_view(), name='admin-list-all-users'),
    path('hairsol-admin/all-clients/', AdminListAllClientView.as_view(), name='admin-list-all-clients'),
    path('hairsol-admin/all-professionals/', AdminListAllProfessionalView.as_view(), name='admin-list-all-professionals'),
    path('hairsol-admin/all-service-providers/', AdminListAllServiceProviderView.as_view(), name='admin-list-all-service-providers'),
    path('hairsol-admin/new-users/', AdminListNewUserView.as_view(), name='admin-list-new-users'),
    path('hairsol-admin/new-users/by-weekly/', AdminListNewUserForTheWeek.as_view(), name='admin-list-new-users-for-specific-date'),
    path('hairsol-admin/all-booked-appointments/', AdminListAllAppointmentView.as_view(), name='admin-list-all-booked-appointments'),
    path('hairsol-admin/all-new-appointments/', AdminListAllNewBookedAppointmentView.as_view(), name='admin-list-all-pending-appointments'),
    path('hairsol-admin/all-completed-appointments/', AdminListAllCompletedAppointmentView.as_view(), name='admin-list-all-completed-appointments'),
    path('hairsol-admin/service-provider/<str:business_name>/', RetrieveUpdateDeleteServiceProviderView.as_view(), name='admin-retrieve-update-delete-service-provider'),
    path('hairsol-admin/create-service-provider/', CreateServiceProviderView.as_view(), name='admin-create-service-provider'),
    path('hairsol-admin/user-activity/', UserActivityView.as_view(), name='admin-user-activity'),
]