from django.urls import path
from . import views

urlpatterns = [
    path("", views.price_to_area, name='price_to_area'),
]
