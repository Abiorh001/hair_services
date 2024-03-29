# Generated by Django 4.1.7 on 2023-12-21 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0004_alter_product_product_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment_booking', '0004_alter_appointment_notes'),
        ('professional_service_provider', '0004_remove_serviceprovideravailabledate_available_times_and_more'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProviderServicesTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_commision', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_provider_earning', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment_checkout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment_booking.appointmentcheckout')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professional_service_provider.serviceproviderprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderProductsTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_commision', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_provider_earning', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('product_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productorder')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professional_service_provider.serviceproviderprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
