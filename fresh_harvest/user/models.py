from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=6)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    default_address = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class WishList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="wishlist"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wish List"


class WishListItem(models.Model):
    # To avoid circular dependency
    from store.models import Product

    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} in {self.wishlist.user.username}'s Wish List"


class WalletTransaction(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet")

    def __str__(self):
        return f"{self.title} - {self.user}"
