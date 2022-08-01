from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('get_all_products/', views.ProductList.as_view()),
    path('product/<int:pk>', views.ProductApiView.as_view()),
    path('get_order_history/', views.OrderHistory.as_view()),
    path('get_order/<int:pk>', views.OrderDetail.as_view()),
    path('get_all_carts/', views.AllCartsApiView.as_view()),
    path('get_cart/', views.CartDetailApiView.as_view()),
]
