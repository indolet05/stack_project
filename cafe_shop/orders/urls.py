from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    # path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('create/', views.create_order, name='create_order'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]