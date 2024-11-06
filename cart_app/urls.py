from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart'),  # Your cart page view
    path('add_cart/<int:id>', views.add_to_cart, name='add_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]
