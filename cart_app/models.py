from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.id}"

    def get_total(self):
        return sum(item.get_total() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        return self.quantity * self.product.price