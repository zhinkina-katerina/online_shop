from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from products.models import Product
from .cart_manager import CartManager

Redis = settings.REDIS


class CartView(TemplateView):
    template_name = 'carts/home.html'
    success_url = '/thanks/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_hex = None
        self.cart = None

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        self.cart_hex, self.cart = CartManager.get_or_create_cart(self.request)
        if not self.cart:
            return context
        context['products'], context['total'] = Product.objects.get_products_with_quantity_and_total(self.cart)
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(CartView, self).render_to_response(context, **response_kwargs)
        if not self.cart:
            response.set_cookie('cart_hex', self.cart_hex)
        return response


class EditCart(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quantity = None
        self.cart_hex = None
        self.cart = None
        self.product_id = None

    def post(self, request):
        self.product_id = request.POST.get('product_id')
        self.quantity = request.POST.get('quantity')
        self.cart_hex, self.cart = CartManager.get_or_create_cart(request)

    def dispatch(self, request, *args, **kwargs):
        response = super(EditCart, self).dispatch(request, *args, **kwargs)
        response.set_cookie('cart_hex', self.cart_hex)
        return response


class UpdateCart(EditCart):
    def post(self, request):
        super(UpdateCart, self).post(request)
        CartManager.update_cart(self.cart_hex, self.cart, item={
            'product': self.product_id,
            'quantity': self.quantity
        })
        return redirect('carts:home')


class RemoveCart(EditCart):
    def post(self, request):
        super(RemoveCart, self).post(request)
        CartManager.remove_product_from_cart(self.cart_hex, self.product_id)
        return redirect('carts:home')
