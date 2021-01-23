from django.urls import path
from .api import ListBookView, CreateCartView, discard
from .views import home

urlpatterns = [
    path('books/', ListBookView.as_view(), name="list_books"),
    path('cart/', CreateCartView.as_view(), name="cart"),
    path('discard/', discard, name="discard"),
    path('home/', home, name="home"),
]
