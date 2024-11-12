from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Address, Order, Order_confirm, OrderItem
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
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'ordered_items.html', {'orders': orders})


