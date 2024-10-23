from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import os
import uuid
from image_cropping import ImageCropField, ImageRatioField
from django.db.models import Case, When, F, FloatField
from decimal import Decimal
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    last_methodOtp = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    title = models.CharField(max_length=350, db_index=True)
    added_on = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_category", args={self.slug})


class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=150)

    def __str__(self):
        return self.variant_name


class Product(models.Model):
    quantity_type = models.ForeignKey(QuantityVariant, on_delete=models.PROTECT)
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = ImageCropField(upload_to="images/")
    image_ratio = ImageRatioField("image", "400x400")
    is_active = models.BooleanField(default=True)
    current_stock = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # This is for the image zooming feature in the detail product view for the user

    def get_file_name(self):
        image_name = os.path.basename(self.image.name)
        return image_name

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product-info", args={self.slug})

    def get_highest_discount_percentage(self):
        # Define a Case expression to check for the highest discount percentage
        max_discount = Case(
            When(
                category__categoryoffers__discount_percentage__gt=F(
                    "productoffers__discount_percentage"
                ),
                then=F("category__categoryoffers__discount_percentage"),
            ),
            default=F("productoffers__discount_percentage"),
            output_field=FloatField(),
        )

        # Retrieve the highest discount percentage for this product
        highest_discount_percentage = (
            Product.objects.filter(pk=self.pk)
            .annotate(max_discount=max_discount)
            .values_list("max_discount", flat=True)
            .first()
        )

        return highest_discount_percentage

    def get_discounted_price(self):
        # Get the highest discount percentage
        highest_discount_percentage = self.get_highest_discount_percentage()

        if highest_discount_percentage is not None:
            # Calculate the discounted price
            discounted_price = self.price - (
                self.price * Decimal(highest_discount_percentage) / Decimal(100)
            )
            return discounted_price
        else:
            # No discount available
            return 0


class Seller(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_profile"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


# authors and books ; many to many rel


class Books(models.Model):
    title = models.CharField(max_length=150)
    published_on = models.DateField()
    review = models.IntegerField(max_length=10)
    author = models.ManyToManyField("Authors")


class Authors(models.Model):
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    book = models.ManyToManyField(Books)
