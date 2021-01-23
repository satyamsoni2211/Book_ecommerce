import os
import django
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book_Ecommerce.settings")

django.setup()

from inventory.models import Book, Cart, CartBox
from inventory.serializer.serializer import CartSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from authentication.models import User

model: User = get_user_model()

user = model.objects.get(username="satyam")

book = Book.objects.first()
cartbox1 = CartBox.objects.create(book=book, quantity=1)
cart: Cart = Cart.objects.create(user=user)
cart.box.set([cartbox1,])
print(CartSerializer(cart).data)
