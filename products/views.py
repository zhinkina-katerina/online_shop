from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


class CategoryListView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Category.objects.all()[:9]
        list_coordination = [{'left': 0, 'top': 0},
                             {'left': 33.2912, 'top': 0},
                             {'left': 66.6456, 'top': 0},
                             {'left': 66.6456, 'top': 469},
                             {'left': 0, 'top': 527},
                             {'left': 33.2912, 'top': 749},
                             {'left': 66.6456, 'top': 938},
                             {'left': 0, 'top': 1055},
                             {'left': 33.2912, 'top': 1219},]
        for i, item in enumerate(queryset):
            item.left = list_coordination[i]['left']
            item.top = list_coordination[i]['top']
        return queryset


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
