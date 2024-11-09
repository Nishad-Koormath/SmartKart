from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipping_address, name='shipping_address'),
    path('payment/', views.payment, name='payment'),
    path('successful/', views.order_successful, name='successful'),
    
]