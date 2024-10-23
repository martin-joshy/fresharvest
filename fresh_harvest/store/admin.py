from django.contrib import admin
from .models import Product, Category, QuantityVariant, Profile, Seller

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(QuantityVariant)
admin.site.register(Profile)
admin.site.register(Seller)
