from django.db import models
from inventory.models import Cart
from django.contrib.auth import get_user_model


# Create your models here.
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=False, null=False)
    address = models.CharField(max_length=1000)
    order_id = models.CharField(max_length=200)
    payment_request_id = models.CharField(primary_key=True, max_length=1000)
    status = models.CharField(max_length=1000)
    instrument_type = models.CharField(max_length=1000)
    billing_instrument = models.CharField(max_length=1000)
    long_url = models.CharField(max_length=1000)
    completed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
