from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'


    def __str__(self):
        return 'Shipping Address - ' + str(self.id)
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.TextField(max_length=10000)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order - #' + str(self.id)
    

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return 'Order Item - #' + str(self.id)


