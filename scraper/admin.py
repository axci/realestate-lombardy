from django.contrib import admin

# Register your models here.
from .models import Apartment

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'province', 'city', 'price', 'area', 'condition', 'latitude', 'longitude']
    list_filter = ['province', 'city', 'price', 'area', 'created', 'condition']
    search_fields = ['title', 'province', 'city']
    ordering = ['province', 'city', 'price', 'area', 'created', 'condition', 'latitude', 'longitude']