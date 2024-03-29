from django.urls import path
from appointment_booking import views


urlpatterns = [
    path('book-appointments/', views.UserBookedAppointmentView.as_view(),
         name='appointment-booked'),
    path('book-appointments/all-appointments/', views.UserBookedAppointmentListView.as_view(),
         name='my-appointments'),
    path('book-appointments/<int:pk>/',
         views.RetrieveUpdateDestroyUserBookedAppointmentView.as_view(),
         name='my-appointment'),
    path('book-appointments/active-appointments/', views.ListUserAllActiveAppointmentView.as_view(),
         name='user-pending-appointments'),
    path('book-appointments/appointments-history/', views.ListUserBookedAppointmentHistoryView.as_view(),
         name='user-appointments-history'),
]
