import requests
from django.shortcuts import render
from django.http import HttpRequest
from .models import Cart
from payments.models import Order


# Create your views here.

def home(request: HttpRequest):
    return render(request, "home.html")


def checkout(request: HttpRequest, cart_id: str):
    cart = Cart.objects.get(cart_id=cart_id)
    Order.objects.filter(cart=cart).delete()
    return render(request, template_name="checkout.html", context={"cart": cart})


def thankyou(request: HttpRequest):
    payment_request_id = request.GET.get("payment_request_id")
    payment_status = request.GET.get("payment_status")  # Credit
    print(f"payment_status; {payment_status}")
    order = Order.objects.get(payment_request_id=payment_request_id)
    success = True
    if payment_status == "Credit":
        order.cart.is_checked_out = True
        order.cart.billed_at = order.completed_at
        order.cart.save()
    else:
        success = False
    return render(request, "thankyou.html", context={"order": order, "success": success, "status": payment_status})
