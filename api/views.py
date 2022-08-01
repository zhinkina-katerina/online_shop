from rest_framework import generics
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from carts.cart_manager import CartManager
from orders.models import Order
from products.models import Product
from .exceptions import CartNotFoundException, NotSpecifiedCartHex
from .permissions import AdminOrReadOnly, OnlyOwner
from .serializers import ProductSerializer, OrderSerializer, CartHexSerializer, CartSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AdminOrReadOnly,)


class OrderHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = Token.objects.get(key=self.request.auth).user_id
        return Order.objects.filter(customer__user=user)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (OnlyOwner, IsAdminUser)


class AllCartsApiView(views.APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        carts = [{'cart_hex': x} for x in CartManager.get_all_carts()]
        results = CartHexSerializer(carts, many=True).data
        return Response(results)


class CartDetailApiView(views.APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        if not request.POST.get('cart_hex'):
            raise NotSpecifiedCartHex
        cart = CartManager.get_or_return_None(request.POST.get('cart_hex'))
        if not cart:
            raise CartNotFoundException
        products = Product.objects.get_products_with_id_in(cart.keys())
        product_list = [{'product_title': x.title, 'product_id': x.id, 'quantity': cart[str(x.id)]} for x in products]
        results = CartSerializer(product_list, many=True).data
        return Response(results)
