# Generated by Django 4.1.5 on 2023-01-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_alter_apartment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='house_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='link',
            field=models.URLField(default='', unique=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
