from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    
]