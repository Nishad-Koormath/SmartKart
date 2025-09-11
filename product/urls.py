from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products_list, name='products' ),
    path('login/',views.login , name='login'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('details/<int:id>/', views.details, name='details'),
]