from django.contrib import admin
from .models import Address, Region, WishListItem, WishList, WalletTransaction

admin.site.register(Address)
admin.site.register(Region)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(WalletTransaction)