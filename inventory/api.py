from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     UpdateAPIView, DestroyAPIView, RetrieveAPIView, get_object_or_404)
from .models import Book, Cart, CartBox
from .serializer.serializer import BookSerializer, CartSerializer, CreateApiDataSerializer
from .paginator import StandardResultsSetPagination
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from pprint import pprint
from rest_framework.decorators import api_view, parser_classes, authentication_classes
from rest_framework.exceptions import APIException


class ListBookView(ListAPIView):
    queryset = Book.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ["title", ]

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        order = self.request.query_params.get("order")
        if order:
            key = "-average_rating" if order == "desc" else "average_rating"
            queryset = queryset.order_by(key)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class CreateCartView(CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = CartSerializer
    parser_classes = [JSONParser, ]
    validator_serializer = CreateApiDataSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Cart.objects.all()
    lookup_field = "cart_id"

    def create(self, request: Request, *args, **kwargs):
        serializer = self.validator_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        pprint(data)
        cart = Cart.objects.create(user=request.user)
        for i in data.get("books"):
            box, created = CartBox.objects.get_or_create(book=Book.objects.get(pk=i.get("id")),
                                                         quantity=i.get("quantity"))
            cart.box.add(box)
        cart_data = self.serializer_class(cart)
        headers = self.get_success_headers(cart_data.data)
        return Response(cart_data.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.query_params[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request: Request, *args, partial=False, **kwargs):
        instance: Cart = self.queryset.get(cart_id=self.request.data.get("cart_id"))

        serializer = self.validator_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        boxes = []
        for i in serializer.data.get("books"):
            box, created = CartBox.objects.get_or_create(book=Book.objects.get(pk=i.get("id")),
                                                         quantity=i.get("quantity"))
            boxes.append(box)
        if not partial:
            instance.box.set(boxes, clear=True)
        else:
            for i in boxes:
                try:
                    print(f"book__title={i.book.title}")
                    instance.box.filter(book__title=i.book.title).delete()
                    instance.box.add(i)
                except:
                    continue
        return Response(CartSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        return self.update(request, *args, partial=True, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE", ])
@authentication_classes([IsAuthenticated, ])
def discard(request: Request):
    cart_id = request.QUERY_PARAMS.get("cart_id")
    if not cart_id:
        raise APIException("Cart Id not provided")
    try:
        Cart.objects.get(cart_id=cart_id).delete()
    except Exception as e:
        raise APIException(str(e))
    return Response({"message": "discarded"})
