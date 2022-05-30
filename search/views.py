from django.views.generic import ListView
from products.models import Product

class SearchProductListView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchProductListView, self).get_context_data(**kwargs)
        context['query']=self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.none()