from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Category
from django.utils import timezone


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productoffers')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.title} - {self.discount_percentage}% off"


class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categoryoffers')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category.name} - {self.discount_percentage}% off"


class ReferralOffer(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_offers')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_redeemed = models.BooleanField(default=False)


    def __str__(self):
        return f"Referral offer from {self.referrer.username} to {self.referred_user.username}"
