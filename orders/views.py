from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import FormView, TemplateView

from carts.cart_manager import CartManager
from online_shop.settings import ADMIN_MAIL
from .forms import CheckoutForm
from .models import Order, Customer, Product
from .product_order_model import ProductsInOrder


class CheckoutView(FormView):
    form_class = CheckoutForm
    template_name = 'orders/checkout_form.html'
    success_url = 'orders:success'
    model = Customer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_delete_cookies = False

    def post(self, request, *args, **kwargs):
        cart_hex, cart = CartManager.get_or_create_cart(request)
        try:
            customer = Customer.objects.get(id=request.user.id)
            customer.first_name = request.POST['first_name']
            customer.last_name = request.POST['last_name']
            customer.phone_number = request.POST['phone_number']
            customer.email = request.POST['email']
            customer.city = request.POST['city']
            customer.address = request.POST['address']
            customer.save()
        except:
            customer = Customer.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                phone_number=request.POST['phone_number'],
                email=request.POST['email'],
                city=request.POST['city'],
                address=request.POST['address']
            )
        if request.user.is_authenticated:
            customer.user = request.user
            customer.save()
        products, total_price = Product.objects.get_products_with_quantity_and_total(cart)
        order = Order.objects.create(
            status='New',
            customer=customer,
            total_price=total_price,
        )
        order.save()

        for product in products:
            ProductsInOrder.objects.create(
                order=order,
                product=product,
                quantity=product.quantity
            )

        CartManager().remove_cart(cart_hex)
        self.can_delete_cookies = True
        self.send_email(order)
        return HttpResponseRedirect(reverse(self.get_success_url()))

    def dispatch(self, request, *args, **kwargs):
        response = super(CheckoutView, self).dispatch(request, *args, **kwargs)
        if self.can_delete_cookies:
            response.delete_cookie('cart_hex')
        return response

    def send_email(self, order):
        send_mail(
            subject=f'New order {order.id}',
            message=f'''You have new order {order.id} ''',
            from_email=ADMIN_MAIL,
            recipient_list=[ADMIN_MAIL],
            fail_silently=False,
        )


class SuccessOrder(TemplateView):
    template_name = 'orders/success.html'
