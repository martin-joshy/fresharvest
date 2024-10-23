from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    country = models.CharField(_("Country"), max_length=255, default="US")


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    sku = models.CharField(_("SKU"), max_length=255)


class Sales(models.Model):
    doc_date = models.DateTimeField(_("date"), db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        _("Quantity"), max_digits=19, decimal_places=2, default=0
    )
    price = models.DecimalField(_("Price"), max_digits=19, decimal_places=2, default=0)
    value = models.DecimalField(_("Value"), max_digits=19, decimal_places=2, default=0)