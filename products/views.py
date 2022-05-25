from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Product

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context


# Create your views here.
