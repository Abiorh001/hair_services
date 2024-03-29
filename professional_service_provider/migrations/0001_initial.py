# Generated by Django 4.1.7 on 2023-12-06 00:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service_categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProviderAvailableTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('service_provider_subscription', models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium')], default='basic', max_length=50)),
                ('business_name', models.CharField(max_length=100, unique=True)),
                ('business_description', models.TextField(blank=True, null=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('business_picture', models.ImageField(blank=True, null=True, upload_to='service_provider_shop_pictures/')),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('business_address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service_offered', models.ManyToManyField(related_name='service_offered', to='service_categories.servicecategory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderAvailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('available_times', models.ManyToManyField(blank=True, related_name='service_provider_available_times', to='professional_service_provider.serviceprovideravailabletime')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('available_dates', models.ManyToManyField(blank=True, related_name='service_provider_available_dates', to='professional_service_provider.serviceprovideravailabledate')),
            ],
        ),
    ]
