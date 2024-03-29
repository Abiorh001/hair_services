from django.apps import AppConfig


class AppointmentBookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment_booking'

    def ready(self):
        import appointment_booking.signals
