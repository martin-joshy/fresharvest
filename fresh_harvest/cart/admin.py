from django.contrib import admin
from .models import Cart, CartItem, Coupon, Order



admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Cart)
admin.site.register(Order)