from django.views.generic import ListView, DetailView

from .models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context




class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk)
