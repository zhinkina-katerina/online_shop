from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


class CategoryListView(ListView):
    template_name = 'index.html'
    queryset = Category.objects.all()


class ProductsByCategoryView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs.get('pk'))


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    queryset = Product.objects.get_active()


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=slug, active=True)
