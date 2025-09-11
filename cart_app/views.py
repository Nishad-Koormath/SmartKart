from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.http import Http404
from django.urls import reverse


@login_required
@require_POST
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    # return redirect('cart')
    return redirect(reverse('details', args=[id]))

# @login_required
def cart_page(request):
    user= request.user
    if  user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.cartitem_set.all() if cart else []

        subtotal = sum(item.get_total() for item in cart_items) 
        shipping = Decimal(5.00) 
        total = subtotal + shipping

        return render(request, 'cart/cart.html', {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
        })
    else:
        return render(request, 'cart/not_login.html')

@login_required
@require_POST
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
@require_POST
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

@login_required
@require_POST
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')
