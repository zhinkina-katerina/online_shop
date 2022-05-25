from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
]