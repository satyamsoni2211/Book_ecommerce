from rest_framework import serializers
from inventory.models import Book, Cart, CartBox
from authentication.serializers.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CartBoxSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = CartBox
        fields = ('book', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    box = CartBoxSerializer(many=True)
    user = UserSerializer()
    total = serializers.SerializerMethodField()

    def get_total(self, instance: Cart):
        return instance.total

    class Meta:
        model = Cart
        fields = '__all__'


class BookCartSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1)


class CreateApiDataSerializer(serializers.Serializer):
    books = BookCartSerializer(many=True)
    user = serializers.IntegerField(required=False)
    cart_id = serializers.CharField(required=False)
