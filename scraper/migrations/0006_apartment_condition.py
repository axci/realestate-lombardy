# Generated by Django 4.1.5 on 2023-01-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_apartment_city_apartment_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='condition',
            field=models.CharField(default='', max_length=50),
        ),
    ]
