from django.contrib import admin # type: ignore
from .models import Product

# Register your models here.
admin.site.register(Product)
