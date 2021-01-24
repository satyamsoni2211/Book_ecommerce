from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from inventory.models import Cart
from .models import Order
from . import api
from pprint import pprint
from django.utils import timezone


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
@parser_classes([FormParser, JSONParser])
def generate_payment_url(request: Request):
    address = request.data.get("address")
    domain = request.data.get("domain")
    cart_id = request.data.get("cart_id")

    cart: Cart = Cart.objects.get(cart_id=cart_id)
    user = request.user
    # Create a new Payment Request
    payload = dict(amount=cart.total,
                   purpose='Books buy',
                   send_email=True,
                   email=user.email,
                   webhook=f"{domain}/webhook/",
                   redirect_url=f"{domain}/thankyou/"
                   )
    response = api.payment_request_create(
        **payload
    )
    payment_request = response.get("payment_request")

    order = Order.objects.create(
        cart=cart,
        address=address,
        payment_request_id=payment_request.get("id"),
        status=payment_request.get("status"),
        long_url=payment_request.get("longurl")
    )

    # print the unique ID(or payment request ID)
    # print(response['payment_request']['id'])
    return Response(data={
        "url": order.long_url
    })


@permission_classes([AllowAny, ])
@api_view(["POST"])
@parser_classes([FormParser, JSONParser])
def webhook(request: Request):
    payment_request = api.payment_request_status(request.data.get("payment_request_id")).get("payment_request")
    payment = payment_request.get("payments")[0]
    order: Order = Order.objects.get(payment_request_id=payment_request.get("id"))
    order.status = payment_request.get("status")
    order.order_id = payment.get("payment_id")
    order.instrument_type = payment.get("instrument_type")
    order.billing_instrument = payment.get("billing_instrument")
    order.completed_at = timezone.now()
    order.save()
    return Response({"message": "received"})
