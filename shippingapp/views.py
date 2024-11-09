from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Address, Order
from .forms import addressForm
from cart_app.models import Cart
from decimal import Decimal
from django.utils import timezone
import uuid

# Create your views here.
@login_required
def shipping_address(request):
    # saved_address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        # Check if a saved address was selected
        # selected_address_id = request.POST.get('selected_address')
        # if selected_address_id:
        #     selected_address = Address.objects.get(id=selected_address_id, user=request.user)
        #     # Handle the selected address (e.g., save it to the order or proceed with it)
        #     return redirect('success')  # Redirect to the payment page or next step in checkout

        # # If no saved address is selected, process the new address form
        form = addressForm(request.POST)
        if form.is_valid():
            address_instance  = form.save(commit=False)
            address_instance.user = request.user
            address_instance.save()
            return redirect('payment')
    else:
        form = addressForm()
    context = {'form': form,
            #    'saved_address': 
            }
    return render(request, 'shipping.html', context)



@login_required
def payment(request):
    if request.method == 'POST':
        return render(request, 'order_success.html')
    else:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.cartitem_set.all()
        subtotal = sum(item.get_total() for item in cart_items)
        shipping = Decimal(5.00) if cart_items else Decimal(0.00)
        total = subtotal + shipping
    return render(request, 'payment.html',{
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
    
    # Create a new Order instance
    order = Order.objects.create(
        user=request.user,
        address= address,  # Assuming the first address is used
        order_id=order_number,
        total_amount=total,
        order_date=timezone.now(),
        status="pending"
    )
    print(f"Order ID: {order.order_id}")
    print(f"Order Date: {order.order_date}")
    print(f"Total Amount: {order.total_amount}")
    # Clear cart items if order is successful
    cart.cartitem_set.all().delete()
    
    return render(request, 'order_success.html', {
        'order_number': order.order_id,
        'order_date': order.order_date,
        'total': order.total_amount
    })
