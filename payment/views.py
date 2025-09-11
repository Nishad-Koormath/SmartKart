from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart_app.models import Cart
from decimal import Decimal
from django.utils import timezone
import uuid

# Create your views here.

@login_required
def payment(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('home')  # Redirect to home if no cart exists

    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.get_total() for item in cart_items)
    shipping = Decimal(5.00) if cart_items else Decimal(0.00)
    total = subtotal + shipping
    order_id = uuid.uuid4().hex[:8].upper()
    

    


    if request.method == 'POST':
        # Create the order confirmation
        order_confirm = Order_confirm.objects.create(user=request.user,order_id=order_id)

        # Clear cart items after successful payment
        cart.cartitem_set.all().delete()

        return render(request, 'order_success.html', {
            'order_date': order_confirm.order_date,
            'order_id' : order_confirm.order_id,
            'total': total,            
            
        })

    # For GET requests, show the payment page with totals
    return render(request, 'payment.html', {
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })

@login_required
def order_successful(request):
    
    cart = Cart.objects.filter(user=request.user).first()
    if not cart :
        return redirect('home')
    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.get_total() for item in cart_items)
    shipping = Decimal(5.00) if cart_items else Decimal(0.00)
    total = subtotal + shipping
    
    # Generate a unique order number
    order_number = uuid.uuid4().hex[:8].upper()
    
    # Get the user's address or fallback to the first address
    address = Address.objects.filter(user=request.user).first()
    
    # Create an Order_confirm instance (you can store the order date here)
    order_confirm = Order_confirm.objects.create(user=request.user)
    
    # Create a new Order instance
    order = Order.objects.create(
        user=request.user,
        address= address,  # Assuming the first address is used
        order_id=order_number,
        total_amount=total,
        order_date=order_confirm,  # Link the order to the Order_confirm instance
        status="pending"
    )
    
        # Create OrderItems for each item in cart
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    
    # Clear cart items if order is successful
    cart.cartitem_set.all().delete()
    ordered_items = Order.objects.filter(user= request.user)

    
    return render(request, 'order_success.html', {
        'order_number': ordered_items.order_id,
        'order_date': ordered_items.order_date,
        'total': ordered_items.total_amount
    })



