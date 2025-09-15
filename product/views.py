from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def home(request):
    latest_products = Product.objects.all()[:6] 
    return render(request, 'products/home.html', {'latest_products': latest_products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/products_list.html', {'products': products})

def product_details(request,id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_details.html', {'product': product})

def contact(request):
    return render(request, 'contact/contact.html')

def about(request):
    return render(request, 'about/about.html')
