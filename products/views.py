from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Product


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Product.objects.get_active()




class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found ((')
        except Product.MultipleObjectsReturned:
            queryset = Product.objects.filter(slug=slug, active=True)
            return queryset.first
        except:
            raise Http404
        return instance
