from django.contrib import admin
from django.urls import path, include
from .views import checkin

urlpatterns = [
    path('checkin', lambda r: checkin(r, None), name='checkin'), # No event
    path('checkin/<event_name>', checkin, name='checkin'),
]