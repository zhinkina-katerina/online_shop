from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):

    def create_new(self, user=None):
        user_object = None
        if user is not None:
            if user.is_authenticated:
                user_object = user
        return self.model.objects.create(user=user_object)

    def get_or_create(self, request):
        cart_id = request.session.get('cart_id', None)
        queryset = self.get_queryset().filter(id=cart_id)

        if queryset.count() == 1:
            is_new_object = False
            cart_object = queryset.first()
            if request.user.is_authenticated and cart_object.user is None:
                cart_object.user = request.user
                cart_object.save()
        else:
            is_new_object = True
            cart_object = self.create_new(user=request.user)
            request.session['cart_id'] = cart_object.id
        return cart_object, is_new_object




class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)