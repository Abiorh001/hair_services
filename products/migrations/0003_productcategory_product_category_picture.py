# Generated by Django 4.1.7 on 2023-12-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='product_category_picture',
            field=models.ImageField(blank=True, null=True, upload_to='product_category_pictures/'),
        ),
    ]
