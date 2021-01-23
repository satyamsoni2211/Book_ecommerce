from time import time
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from hashlib import md5
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.

class Book(models.Model):
    bookID = models.IntegerField(db_index=True, null=False, blank=True, primary_key=True)
    title = models.CharField(blank=False, null=False, db_index=True, max_length=200)
    authors = models.CharField(blank=False, null=False, max_length=200)
    average_rating = models.FloatField()
    isbn = models.CharField(max_length=200)
    language_code = models.CharField(max_length=200)
    ratings_count = models.IntegerField()
    price = models.FloatField(blank=False, null=False)
    image = models.CharField(blank=False, null=False, max_length=1000)

    def __str__(self):
        return f"{self.bookID} {self.title}"

    def __repr__(self):
        return f"{self.bookID} {self.title}"

    class Meta:
        db_table = "Books"
        ordering = ("bookID",)
        unique_together = ("bookID", "title")


class CartBox(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name="box", related_query_name="box")
    quantity = models.IntegerField(default=1, null=False, blank=False)
    box_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "cartbox"

    def __str__(self):
        return f"{self.book.title} {self.quantity}"


class Cart(models.Model):
    cart_id = models.CharField(primary_key=True, max_length=200)
    box = models.ManyToManyField(CartBox, related_name="cart",
                                 related_query_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    is_discarded = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    billed_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )

    @property
    def total(self):
        return sum(i.book.price * i.quantity for i in self.box.all())

    def __str__(self):
        return f"{self.user.username} {self.pk}"

    class Meta:
        db_table = "cart"
        ordering = ('-created_at',)


@receiver(pre_save, sender=Cart)
def populate_id(sender: Cart, instance: Cart, *args, **kwargs):
    if not instance.cart_id:
        print(f"populating cart id")
        instance.cart_id = md5(f"cart_{time()}".encode()).hexdigest()
