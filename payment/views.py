from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart_app.models import Cart
from decimal import Decimal
import uuid
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from shippingapp.models import Address, Order_confirm, Order, OrderItem
from django.utils import timezone
import json

@login_required
def payment(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('home')

    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.get_total() for item in cart_items)
    shipping = Decimal(5.00) if cart_items else Decimal(0.00)
    total = subtotal + shipping
    amount_in_paise = int(total * 100)

    if request.method == 'GET':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': 1
        })

        return render(request, 'payment.html', {
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': order['id'],
            'amount_in_paise': amount_in_paise
        })


@csrf_exempt
@login_required
def verify_payment(request):
    data = json.loads(request.body)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    params_dict = {
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    }

    try:
        client.utility.verify_payment_signature(params_dict)
    except:
        return JsonResponse({'status': 'failure'}, status=400)

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.get_total() for item in cart_items)
    shipping = Decimal(5.00) if cart_items else Decimal(0.00)
    total = subtotal + shipping
    order_number = uuid.uuid4().hex[:8].upper()
    address = Address.objects.filter(user=request.user).first()

    order_confirm = Order_confirm.objects.create(user=request.user, order_id=order_number)

    order = Order.objects.create(
        user=request.user,
        address=address,
        order_id=order_number,
        total_amount=total,
        order_date=timezone.now(),
        status='pending'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.cartitem_set.all().delete()

    return JsonResponse({'status': 'success'})