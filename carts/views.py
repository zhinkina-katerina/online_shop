from django.shortcuts import render

from .models import Cart

def view(request):
    cart_object = Cart.objects.get_or_create(request)
    return render(request, 'carts/home.html', {})
