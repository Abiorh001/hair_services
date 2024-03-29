from django.db import models


class ServiceCategory(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, null=False)
    service_category_picture = models.ImageField(upload_to='service_category_pictures/', blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name






