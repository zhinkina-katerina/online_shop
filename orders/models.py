from django.contrib.auth.models import User
from django.db import models

from orders.product_order_model import ProductsInOrder
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('New', 'Новый'),
        ('In_process', 'В процессе'),
        ('Done', 'Выполнен'),
        ('Canceled', 'Отменен'),
    )

    date_creation = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=200)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    products = models.ManyToManyField(Product, through=ProductsInOrder)


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
