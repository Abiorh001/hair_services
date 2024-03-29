from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from datetime import datetime, timedelta

@receiver(post_save, sender=Appointment)
def update_appointment_status(sender, instance, **kwargs):
    print(f"Signal triggered for Appointment ID {instance.id}")
    
    # Check if the status field has changed
    if instance.status == 'booked':
        # Change the status to on-process or on-waiting based on conditions
        appointment_date_time = datetime.combine(instance.date, instance.time)
        time_to_set_on_waiting = appointment_date_time - timedelta(minutes=45)
        time_to_set_on_waiting_start = appointment_date_time - timedelta(minutes=50)
        
        if datetime.now() >= time_to_set_on_waiting_start and datetime.now() < time_to_set_on_waiting:
            new_status = 'on-waiting'
            instance.notes = "Time Estimation: 50 Minutes"
            instance.save()
        elif datetime.now() >= time_to_set_on_waiting:
            new_status = 'on-process'
        else:
            print("No status change needed.")
            return  # No need to change status, exit the function

        if instance.status != new_status:
            print(f"Changing status from {instance.status} to {new_status}")
            instance.status = new_status
            instance.save()
    elif instance.status == 'on-waiting':
        appointment_date_time = datetime.combine(instance.date, instance.time)
        time_to_set_on_process = appointment_date_time
        
        if datetime.now() >= time_to_set_on_process and instance.status != 'on-process':
            print("Changing status from on-waiting to on-process")
            instance.status = 'on-process'
            service = instance.service
            duration_of_service = service.duration_minutes
            instance.notes = f"On Process {duration_of_service} Minutes"
            instance.save()
    elif instance.status == 'on-process':
        appointment_date_time = datetime.combine(instance.date, instance.time)
        service = instance.service
        duration_of_service = service.duration_minutes
        instance.notes = f"On Process {duration_of_service} Minutes"
        added_time = timedelta(minutes=duration_of_service) + timedelta(minutes=1)
        time_to_set_finished = appointment_date_time + added_time
        
        if datetime.now() > time_to_set_finished and instance.status != 'finished':
            print("Changing status from on-process to finished")
            instance.status = 'finished'
            instance.notes = "Appointment Finished"
            instance.save()
    print("Signal processing complete.\n")
