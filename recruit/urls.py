from django.contrib import admin
from django.urls import path, include
from .views import checkin

urlpatterns = [
    path('checkin', checkin, name='checkin'),
]