from django.contrib import admin
from .models import Address, Order, OrderItem, Order_confirm

# Register your models here.
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Order_confirm)


