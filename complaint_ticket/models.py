from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import CustomUser

class ComplaintTicket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_number = models.CharField(max_length=255, blank=False, null=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaint_tickets')
    complaint_text = models.TextField(blank=False, null=False)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.ticket_number} - {self.user.email}"

class ComplaintTicketMessage(models.Model):
    id = models.AutoField(primary_key=True)
    complaint_ticket = models.ForeignKey(ComplaintTicket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.complaint_ticket.ticket_number} - {self.user.email}"
