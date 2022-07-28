from django.urls import path
from . import views
app_name = 'carts'

urlpatterns = [
    path('', views.CartView.as_view(), name='home'),
    path('update/', views.UpdateCart.as_view(), name='update'),
    path('remove/', views.RemoveCart.as_view(), name='remove'),
]