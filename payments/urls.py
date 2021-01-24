from django.urls import path
from .api import generate_payment_url, webhook

urlpatterns = [
    path('generate_payment_url/', generate_payment_url, name="generate_payment_url"),
    path('webhook/', webhook, name="webhook"),
]
