from django.urls import path
from .views import ussd_callback

urlpatterns = [
    path('ussd/', ussd_callback),
]
