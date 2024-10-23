from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from user.models import Address
import uuid



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name = 'cart')
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True )

    def __str__(self):
        return f"{self.user.username} Cart"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




class Order(models.Model):

    # Payment Method Choices
    CASH_ON_DELIVERY = 'COD'
    PAYPAL = 'PayPal'
    
    PAYMENT_METHOD_CHOICES = [
        (CASH_ON_DELIVERY, 'Cash on Delivery'),
        (PAYPAL, 'PayPal'),
    ]

     # Order Status Choices
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    PAYMENT_PENDING = 'payment_pending'
    
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
        (PAYMENT_PENDING, 'payment_pending')
    ]


    #Payment Status 
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    
    PAYMENT_STATUS_OPTIONS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]


    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default=CASH_ON_DELIVERY) 
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_OPTIONS, default=PENDING)
    

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total_price(self):
        total_price = sum(item.price * item.qty for item in self.orderitem_set.all())
        return total_price
    
    def grand_total(self):
        total_discount = sum(item.discount * item.qty for item in self.orderitem_set.all())
        grand_total = self.calculate_total_price() - abs(total_discount) - self.coupon_discount
        return grand_total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # discount (amount) given for a product 
                                                                               # particular product per unit at the time of order

    def __str__(self):
        return f"{self.qty} x {self.product.title} in Order #{self.order.id}"

    

class Coupon(models.Model):
    coupon_code= models.CharField(max_length = 10)
    is_expired= models.BooleanField(default = False)
    discount_price= models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default = 500)

    def __str__(self):
        return self.coupon_code