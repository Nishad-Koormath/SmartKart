from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "addresses")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=250)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order_confirm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20, default='Null')
    def __str__(self):
        return f"{self.user} {self.order_date}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.ForeignKey(Order_confirm, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=10, unique= True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered")])
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self) :
        return f"Order {self.order_id} - {self.user.first_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.order.order_id})"

    def get_total_price(self):
        return self.quantity * self.price
    
