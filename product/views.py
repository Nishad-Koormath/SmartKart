from django.shortcuts import render
from .models import Product
import accounts_app

# Create your views here.

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:6]  # Display latest 5 products
    return render(request, 'products/home.html', {'latest_products': latest_products})

def products_list(request):
    products = Product.objects.all()
    return render(request, 'products/products_list.html', {'products': products})
def login(request):
    print('login page')
    return render(request, 'accounts_app/accounts/login.html')
def contact(request):
    return render(request, 'contact/contact.html')
def about(request):
    return render(request, 'about/about.html')
def details(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_details.html', {'product': product})


