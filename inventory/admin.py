from django.contrib import admin
from .models import Cart, CartBox, Book

# Register your models here.
admin.site.register(Cart)
admin.site.register(Book)
admin.site.register(CartBox)
