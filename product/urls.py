from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products_list, name='products' ),
    path('details/<int:id>/', views.details, name='product_details'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]