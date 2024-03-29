from django.db import models


class UserActivity(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, null=False)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity_type

# Create your models here.
