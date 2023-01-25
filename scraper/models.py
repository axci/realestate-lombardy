from django.db import models
from django.utils import timezone


class Apartment(models.Model):
    house_id = models.IntegerField(default=0)
    title = models.CharField(max_length=120)
    typology = models.CharField(max_length=25, default='')
    price = models.IntegerField()
    area = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)  #auto_now_add the date will be saved automatically when creating an object
    updated = models.DateTimeField(auto_now=True)
    link = models.URLField(default='', unique=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    province = models.CharField(default='', max_length=50)
    city = models.CharField(default='', max_length=50)
    condition = models.CharField(default='', max_length=50)

    class Meta:
        ordering = ['-created']  # Creating a sort order from newest to oldest
        indexes = [  # This will improve performance for queries filtering or ordering results by this field.
            models.Index(fields=['-created']),
        ]

    def __str__(self):  # for human-readable representation of the object
        return self.title