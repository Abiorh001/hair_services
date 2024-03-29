from django.urls import path
from professional_service_provider import views

urlpatterns = [
    path('service-providers/register/', views.CreateServiceProviderProfileView.as_view(),
         name='service-providers-register-profile'),
    path('service-providers/profile/', views.RetrieveUpdateServiceProviderProfileView.as_view(),
         name='retrieve-update-service-provider-profile'),
    path('service-providers/services/', views.ListServiceProviderServiceView.as_view(),
                name='list-service-provider-services'),
    path('service-providers/services/<int:id>/', views.RetrieveUpdateDestroyServiceProviderServiceView.as_view(),
         name='retrieve-update-destroy-service-provider-service'),
    path('service-providers/products/', views.ListServiceProviderProductsView.as_view(),
         name='list-service-provider-services'),
    path('service-providers/set-availability-date-time/', views.ServiceProviderSetAvailabityDayView.as_view(),
         name='set-availability-date-time'),
     path('service-providers/availabilities/', views.ListServiceProviderAvailabilityView.as_view(),
           name='list-service-provider-availabilities'),
    path('service-providers/availabilities/by-date/', views.ListServiceProviderAvailabilityByDateView.as_view(),
         name='list-service-provider-availability-by-date'),
    path('service-providers/availabilities/<int:id>/', views.RetrieveUpdateDestroyServiceProviderAvailabilityView.as_view(),
         name='retrieve-update-destroy-service-provider-availability'),
    path('service-providers/all-booked-appointments/', views.ServiceProviderAllBookedAppointmentsView.as_view(),
         name='service-provider-all-booked-appointments'),
    path('service-providers/all-booked-appointments/by-date/', views.ServiceProviderViewBookedAppointmentByDateView.as_view(),
         name='service-provider-booked-appointments-by-date'),
    path('service-providers/past-booked-appointments/', views.ServiceProviderViewPastBookedAppointmentView.as_view(),
         name='service-provider-past-booked-appointments'),
    path('service-providers/upcoming-appointments/', views.ServiceProviderViewUpcomingBookedAppointmentView.as_view(),
         name='service-provider-upcoming-booked-appointments'),
    path('service-providers/each-appointment/<int:id>/', views.ServiceProviderRetrievedSingleBookedAppointment.as_view(),
          name='service-provider-retrieve-appointment'),

]